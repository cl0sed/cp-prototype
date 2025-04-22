# Multi-Agent System Implementation Plan

**A. Overview**

This plan outlines the phases and steps required to implement the multi-agent architecture, incorporating the decisions made and leveraging the existing project structure and context from the Memory Bank and `README.md`. Each phase includes specific tasks, target files/modules, testing requirements, and documentation updates.

**B. Implementation Phases**

**Phase 0: Preparation & Review (Mandatory First Step)**

1.  **Review Project Context:**
    *   Thoroughly review `README.md` for project goals, architecture, structure, and tech stack.
    *   Review all Memory Bank files (`productContext.md`, `activeContext.md`, `decisionLog.md`, `progress.md`, `systemPatterns.md`) for current status, decisions, and patterns.
    *   Review existing DB models in `backend/app/db/models/` (`User.py`, `Video.py`, `ChatMessage.py`, etc.). Note the removal of several models as per `decisionLog.md` and `progress.md`.
    *   Review existing relevant code (auth in `backend/app/features/auth/`, base API structure in `backend/app/api/routers/`, worker setup in `backend/app/worker/`).
    *   Confirm tech stack versions align with `README.md` (FastAPI 0.115.0+, SQLAlchemy 2.0+, SAQ 0.22.5+, Haystack 2.x, React 19.1, PostgreSQL/pgvector).
2.  **Understand Final Phase 1 Summary:** Internalize the complete multi-agent architecture, agent roles (Platform vs. Video), session model (Platform vs. Video), memory strategy (MVP scope: Working, basic Semantic/Episodic/Artifacts), SSE communication, SAQ task handling (persistence, cancellation, status), and deferred items (rollback logic, advanced memory analysis).

**Phase 1: Backend Foundation - Models, State & Core Services**

*(Goal: Establish the database structure, core state management, basic memory models & tools, SSE backend, and essential APIs)*

1.  **Define/Update Shared Enums:**
    *   Create `backend/app/shared/constants/enums.py`.
    *   Define Python `enum.Enum` classes for:
        *   `VideoStatus` (e.g., `IDEA`, `RESEARCHING`, `SCRIPTING`, `PENDING_HANDOFF_CONFIRMATION`, `EDITING`, `COMPLETE`, `FAILED`)
        *   `SessionType` (`ASSISTANT`, `ONBOARDING`, `VIDEO`)
        *   `AgentType` (`ASSISTANT`, `ONBOARDING`, `RESEARCH`, `SCRIPTING`, etc.)
        *   `ChatMessageRole` (`USER`, `ASSISTANT`, `SYSTEM`)
        *   `ArtifactType` (e.g., `RESEARCH_NOTES`, `SCRIPT_DRAFT`, `VIDEO_IDEA`)
2.  **Implement/Update Database Models (`backend/app/db/models/`):**
    *   **`User.py`:**
        *   Add `is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)`.
    *   **`Video.py`:**
        *   Add `phase: Mapped[str] = mapped_column(String, nullable=True, index=True)` (Consider using `VideoStatus` enum values here or a separate phase enum).
        *   Update `status: Mapped[str] = mapped_column(String, index=True)` -> Ensure it uses `VideoStatus` enum values.
        *   Add `active_agent_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)` (Uses `AgentType` enum values).
        *   Add `active_job_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), nullable=True)` (To link to the currently running SAQ job for cancellation).
        *   *(Rollback placeholder):* Consider adding nullable fields like `previous_phase: Mapped[Optional[str]]`, `rollback_data: Mapped[Optional[dict]] = mapped_column(JSONB)` if needed later.
    *   **Create `ChatSession.py`:**
        *   Define `ChatSession` model inheriting from `Base`.
        *   Fields: `id` (UUID, PK), `user_id` (FK to `users.id`), `video_id` (FK to `videos.id`, nullable), `session_type: Mapped[str]` (Uses `SessionType` enum values), `created_at`, `updated_at`.
        *   Establish relationships (e.g., `user`, `video`, `messages`).
    *   **Update `ChatMessage.py`:**
        *   Rename `session_id` to `chat_session_id` and make it `Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)`.
        *   Ensure `role: Mapped[str]` uses `ChatMessageRole` enum values.
        *   Add relationship back to `ChatSession`.
    *   **Create `UserPreferences.py`:**
        *   Define `UserPreference` model inheriting from `Base`.
        *   Fields: `id` (UUID, PK), `user_id` (FK to `users.id`, unique), `preferences: Mapped[dict] = mapped_column(JSONB, nullable=False, default={})`, `created_at`, `updated_at`.
        *   Establish relationship back to `User`.
    *   **Create `VideoArtifact.py`:**
        *   Define `VideoArtifact` model inheriting from `Base`.
        *   Fields: `id` (UUID, PK), `video_id` (FK to `videos.id`), `artifact_type: Mapped[str]` (Uses `ArtifactType` enum values), `data: Mapped[dict] = mapped_column(JSONB, nullable=False)`, `version: Mapped[int] = mapped_column(Integer, default=1)`, `created_at`, `updated_at`.
        *   Establish relationship back to `Video`. Add index on `(video_id, artifact_type, version)`.
    *   **Create `MemoryAnalyzedEpisode.py`:**
        *   Define `AnalyzedEpisode` model inheriting from `Base`.
        *   Fields: `id` (UUID, PK), `user_id` (FK to `users.id`), `video_id` (FK to `videos.id`, nullable), `chat_session_id` (FK to `chat_sessions.id`, nullable), `timestamp` (DateTime), `summary` (Text), `keywords` (JSONB - could be array of strings), `embedding` (Vector - if using pgvector).
    *   **Update `__init__.py`:** Ensure all new models are imported and added to `__all__`.
    *   **Generate and Apply Alembic Migrations:** Run `alembic revision --autogenerate -m "Implement multi-agent models"` and `alembic upgrade head`. Manually review/edit migration script if needed.
3.  **Implement Shared Memory Tools (`backend/app/shared/tools/memory.py`):**
    *   Create async functions using SQLAlchemy 2.0+ syntax (e.g., `select`, `session.execute`, `session.scalar`).
    *   `get_chat_history(db: AsyncSession, chat_session_id: UUID, limit: int = 20) -> List[ChatMessage]`
    *   `save_chat_message(db: AsyncSession, chat_session_id: UUID, user_id: UUID, role: ChatMessageRole, content: str) -> ChatMessage`
    *   `get_user_preferences(db: AsyncSession, user_id: UUID) -> Optional[UserPreference]`
    *   `update_user_preferences(db: AsyncSession, user_id: UUID, prefs: dict) -> UserPreference` (handles create or update)
    *   `get_video_project_state(db: AsyncSession, video_id: UUID) -> Optional[Video]`
    *   `update_video_project_state(db: AsyncSession, video_id: UUID, **kwargs) -> Video` (updates fields like `status`, `phase`, `active_agent_type`, `active_job_id`)
    *   `save_video_artifact(db: AsyncSession, video_id: UUID, artifact_type: ArtifactType, data: dict) -> VideoArtifact` (potentially handle versioning)
    *   `get_video_artifact(db: AsyncSession, video_id: UUID, artifact_type: ArtifactType, version: Optional[int] = None) -> Optional[VideoArtifact]` (get latest if version is None)
    *   `get_chat_session(db: AsyncSession, chat_session_id: UUID) -> Optional[ChatSession]`
4.  **Implement Core API Endpoints:**
    *   **Video Management (`backend/app/api/routers/video.py`):**
        *   `POST /videos`: Create new video project (initial state, associate with user, create initial `ChatSession` of type `VIDEO`). Return `video_id` and `chat_session_id`.
        *   `GET /videos`: List user's video projects.
        *   `GET /videos/{video_id}`: Get video project details and status.
    *   **Task Cancellation (`backend/app/api/routers/tasks.py`):**
        *   `POST /videos/{video_id}/cancel`: Get `video_id`, find associated `active_job_id` from `Video` model, fetch SAQ job using `active_job_id`, call `job.abort()`. Requires SAQ context/queue access. Handle cases where job is not found or already completed/aborted.
    *   **Chat Session Info (`backend/app/api/routers/chat.py` or `session.py`):**
        *   `GET /sessions/{chat_session_id}`: Get session details (type, associated video/user).
        *   `GET /sessions`: List user's active sessions (Platform + Video).
5.  **Setup SSE Communication (Backend):**
    *   **SSE Router (`backend/app/api/routers/sse.py`):**
        *   `GET /sse/{chat_session_id}`: Endpoint for clients to connect. Requires authentication (e.g., verify user owns the session).
        *   Use a library like `sse-starlette`. Manage connections (add/remove clients for a session_id).
    *   **SSE Publishing Mechanism (`backend/app/shared/sse_publisher.py` or similar):**
        *   Implement a helper class/functions (`publish_to_session(chat_session_id: UUID, event_data: dict)`).
        *   Use Redis Pub/Sub: SAQ tasks publish JSON messages to a Redis channel (e.g., `sse:{chat_session_id}`).
        *   The SSE router (`sse.py`) subscribes to relevant Redis channels when a client connects and forwards messages. Ensure robust handling of connections/disconnections and Redis communication.
        *   Define standard event structure: `{ "type": "message", "payload": {"role": "assistant", "content": "..."} }`, `{ "type": "status", "payload": {"status": "processing", "detail": "Agent X working..."} }`, `{ "type": "error", "payload": {"message": "..."} }`.
6.  **Testing & Documentation (Phase 1):**
    *   Unit tests (`pytest`) for new/modified DB models (using `factory-boy`), enum definitions, memory tools (mocking DB session), state transition logic stubs.
    *   Integration tests for core APIs (video mgmt, task cancellation, SSE connection endpoint). Mock SAQ interactions for cancellation.
    *   Document finalized DB schema (potentially using `sqlalchemy-schemadisplay` or similar). Add Mermaid diagram.
    *   Document core API endpoints (request/response schemas, auth).
    *   Document memory tool function signatures and usage.
    *   Document SSE connection process and event structure.
    *   Update `backend/README.md` and relevant Memory Bank files (`systemPatterns.md`, `decisionLog.md`).

    ```mermaid
    graph TD
        subgraph "Database Schema (Phase 1 MVP)"
            U[User id, email, supertokens_user_id, username, is_onboarded, created_at, role]
            UP[UserPreference id, user_id FK, preferences JSONB, created_at, updated_at]
            V[Video id, title, status (enum), phase (enum), active_agent_type (enum), active_job_id UUID?, created_at, updated_at]
            VA[VideoArtifact id, video_id FK, artifact_type (enum), data JSONB, version INT, created_at, updated_at]
            CS[ChatSession id, user_id FK, video_id FK?, session_type (enum), created_at, updated_at]
            CM[ChatMessage id, chat_session_id FK, user_id FK, role (enum), content TEXT, timestamp, metadata_ JSONB]
            AE[AnalyzedEpisode id, user_id FK, video_id FK?, chat_session_id FK?, timestamp, summary TEXT, keywords JSONB, embedding VECTOR?]
            BJ[BackgroundJob id, job_type, status, project_id(video_id) FK?, user_id FK?, parameters JSONB, result JSONB, error TEXT?, created_at, updated_at, completed_at?]

            U --o{ UP : "preferences (1-1)"
            U --o{ CS : "sessions"
            U --o{ CM : "messages"
            U --o{ AE : "episodes"
            U --o{ BJ : "initiated_jobs"

            V --o{ VA : "artifacts"
            V --o{ CS : "sessions (optional)"
            V --o{ AE : "episodes (optional)"
            V --o{ BJ : "jobs"

            CS --o{ CM : "messages"
            CS --o{ AE : "episodes (optional)"
        end
    ```

**Phase 2: Platform Agent & Workflow Backend Implementation**

*(Goal: Implement Assistant & Onboarding agents, basic Orchestrator logic, API routing, and background task infrastructure)*

1.  **Implement Platform Agent Pipelines & SAQ Tasks:**
    *   **`AssistantAgent` (`backend/app/agents/platform/assistant/`):**
        *   `pipeline.py`: Define Haystack 2.x pipeline. Input: `user_message`, `chat_session_id`, `user_id`. Components: `PromptBuilder` (using system prompt + `get_chat_history`), `OpenAIChatGenerator` (or chosen LLM), `ToolInvoker` (using shared memory tools like `create_video`, `get_user_preferences`). Output: `agent_response`.
        *   `prompts/`: Define system prompt, tool descriptions.
        *   `tools.py`: Define tools (e.g., `create_video_project` wrapper calling video API or service).
        *   `tasks.py`: Define `run_assistant_agent(ctx, chat_session_id: UUID, user_id: UUID, user_message: str)` SAQ task.
            *   Load pipeline.
            *   Fetch history via `get_chat_history`.
            *   Publish initial "Processing..." status via SSE publisher.
            *   Run pipeline. Handle tool calls (publish status updates via SSE).
            *   Save agent response via `save_chat_message`.
            *   Publish final response via SSE publisher.
            *   Handle errors (publish error via SSE).
            *   Periodically check `ctx.job.is_aborted()` for cancellation.
    *   **`OnboardingAgent` (`backend/app/agents/platform/onboarding/`):**
        *   `pipeline.py`: Similar structure to Assistant. Input: `user_message`, `chat_session_id`, `user_id`. Tools might include `update_user_onboarding_status`, `get_user_preferences`, `update_user_preferences`.
        *   `prompts/`: Define onboarding-specific prompts.
        *   `tools.py`: Define tools (e.g., `update_user_onboarding_status` wrapper calling user service/tool).
        *   `tasks.py`: Define `run_onboarding_agent(...)` SAQ task. Similar logic to Assistant task, but calls `update_user_preferences` and potentially triggers an Orchestrator task upon completion via `update_user_onboarding_status` tool.
2.  **Implement Orchestrator Logic & SAQ Tasks (Basic):**
    *   **`backend/app/workflow/orchestrator/logic.py`:**
        *   Define functions like `check_onboarding_status(user: User) -> bool`, `handle_onboarding_completion(user_id: UUID)`.
    *   **`backend/app/workflow/orchestrator/tasks.py`:**
        *   Define `trigger_onboarding_if_needed(ctx, user_id: UUID)`: Called potentially after user creation or first login. Checks `user.is_onboarded`. If false, creates an `ONBOARDING` `ChatSession` and potentially sends an initial message or waits for user interaction.
        *   Define `post_onboarding_transition(ctx, user_id: UUID)`: Called by `OnboardingAgent`'s tool. Updates `user.is_onboarded = True`. May enqueue `AssistantAgent` or notify user.
        *   Define `handle_handoff_confirmation(ctx, video_id: UUID, confirmed_status: VideoStatus)`: Placeholder task triggered by specialized agents later. Updates `Video.status`.
3.  **Implement API Chat Routing Logic (`backend/app/api/routers/chat.py`):**
    *   `POST /chat/{chat_session_id}/message`:
        *   Receive `user_message`, `chat_session_id`.
        *   Use `chat_session_id` to fetch `ChatSession` details (user_id, video_id, session_type) via `get_chat_session`. Authenticate user owns session.
        *   Save user message via `save_chat_message`.
        *   **Routing Logic:**
            *   If `session_type == SessionType.ASSISTANT`, enqueue `run_assistant_agent` SAQ task.
            *   If `session_type == SessionType.ONBOARDING`, enqueue `run_onboarding_agent` SAQ task.
            *   If `session_type == SessionType.VIDEO`:
                *   Fetch `Video` state using `video_id`.
                *   Based on `Video.active_agent_type` (e.g., `AgentType.RESEARCH`), enqueue the corresponding specialized agent SAQ task (e.g., `run_research_agent`). (Requires specialized agent tasks defined in Phase 3).
        *   Return immediately (e.g., `202 Accepted`). Frontend will get updates via SSE.
4.  **Implement Background Task Scheduling (`backend/app/worker/tasks/analysis.py` & `settings.py`):**
    *   Define placeholder SAQ task function `run_episodic_analysis(ctx)` in `analysis.py`.
    *   Configure SAQ cron scheduler in `settings.py` to call `run_episodic_analysis` periodically (e.g., every hour). `cron=[saq.CronJob(run_episodic_analysis, cron="0 * * * *")]`.
5.  **Testing & Documentation (Phase 2):**
    *   Unit/integration tests for Platform Agents (mock LLM/tools/SSE publisher), SAQ tasks (including status publishing, cancellation checks), Orchestrator logic/tasks, API chat routing logic.
    *   Document Platform Agent prompts, tools, task inputs/outputs. Add Mermaid diagram for chat flow.
    *   Document Orchestrator state transitions and triggers.
    *   Document background task scheduling.
    *   Update `backend/README.md`, `systemPatterns.md`, `decisionLog.md`.

    ```mermaid
    sequenceDiagram
        participant FE as Frontend
        participant API as FastAPI API (/chat)
        participant DB as Database
        participant SSEPub as SSE Publisher (Redis)
        participant SAQW as SAQ Worker

        FE->>+API: POST /chat/{session_id}/message (user_message)
        API->>+DB: Get ChatSession (session_id)
        DB-->>-API: Return session (type, user_id, video_id?)
        API->>+DB: Save ChatMessage (user_role)
        DB-->>-API: Confirm save
        alt SessionType == ASSISTANT
            API->>+SAQW: Enqueue run_assistant_agent(session_id, user_id, user_message)
        else SessionType == ONBOARDING
            API->>+SAQW: Enqueue run_onboarding_agent(...)
        else SessionType == VIDEO
            API->>+DB: Get Video(video_id) for active_agent_type
            DB-->>-API: Return Video state
            API->>+SAQW: Enqueue run_specialized_agent(...) based on active_agent_type
        end
        API-->>-FE: 202 Accepted

        Note right of SAQW: Worker picks up task
        SAQW->>+SSEPub: Publish Status: Processing
        SAQW->>+DB: get_chat_history(session_id)
        DB-->>-SAQW: Return history
        Note right of SAQW: Run Haystack Pipeline (LLM, Tools...)
        SAQW->>+DB: (Tool Call) e.g., update_video_project_state()
        DB-->>-SAQW: Confirm update
        SAQW->>+SSEPub: Publish Status: Tool X called...
        Note right of SAQW: Pipeline generates response
        SAQW->>+DB: save_chat_message(agent_response)
        DB-->>-SAQW: Confirm save
        SAQW->>+SSEPub: Publish Message: agent_response
        SAQW->>+SSEPub: Publish Status: Completed
        Note right of SAQW: Task finishes
    ```

**Phase 3: Specialized Agent Foundation & Workflow Refinement**

*(Goal: Set up structure for Video Agents, implement handoff confirmation & cancellation mechanisms)*

1.  **Structure Specialized Agents (`backend/app/agents/video/`):**
    *   Create directories for initial agents (e.g., `research/`, `scripting/`).
    *   Inside each, create placeholder files: `pipeline.py`, `prompts/` (dir), `tools.py`, `tasks.py`.
    *   Define placeholder SAQ task functions in `tasks.py` (e.g., `run_research_agent(ctx, chat_session_id: UUID, user_id: UUID, video_id: UUID, user_message: str)`). These will be called by the chat router in Phase 2.
2.  **Implement Handoff Confirmation Logic:**
    *   **Orchestrator (`workflow/orchestrator/tasks.py`):**
        *   Refine `handle_handoff_confirmation` task. Logic: Update `Video.status` based on user confirmation (received via a specialized agent tool call). If confirmed, potentially update `Video.active_agent_type` to the next agent in sequence and enqueue its task.
    *   **Specialized Agent Tools (Placeholders):**
        *   In placeholder `tools.py` for agents like `Research`, define a tool stub like `propose_handoff_to_scripting(video_id: UUID)`. This tool would update `Video.status` to `PENDING_HANDOFF_CONFIRMATION` and `Video.active_agent_type` to `SCRIPTING` (or similar marker) via `update_video_project_state`. The agent's response would ask the user for confirmation.
    *   **Specialized Agent Task (Handling Confirmation):**
        *   Agent task logic needs to check if the `Video.status` is `PENDING_HANDOFF_CONFIRMATION` for its type. If so, interpret `user_message` as confirmation/rejection. Call an orchestrator task/tool `confirm_handoff(video_id, confirmed: bool)` which triggers `handle_handoff_confirmation`.
3.  **Implement Task Cancellation Mechanism:**
    *   **API Endpoint (`api/routers/tasks.py`):**
        *   Finalize `POST /videos/{video_id}/cancel` logic. Fetch `Video` by `video_id`, get `active_job_id`. Use SAQ's API (e.g., `await queue.job(active_job_id)`) to get the job object, then call `await job.abort()`. Handle errors gracefully (job not found, already finished, etc.). Update `Video.status` to `FAILED` or `CANCELLED`.
    *   **SAQ Tasks (All Agents):**
        *   Ensure agent tasks (`assistant/tasks.py`, `onboarding/tasks.py`, specialized agent `tasks.py`) include periodic checks: `if await ctx.job.is_aborted(): logger.warning("Job aborted"); return` (or raise specific exception). Place checks between significant steps (e.g., before/after LLM calls, tool calls).
4.  **Testing & Documentation (Phase 3):**
    *   Unit/integration tests for handoff state transitions in Orchestrator (mocking agent tool calls).
    *   Integration test for the cancellation API endpoint (mocking SAQ job retrieval/abort).
    *   Unit tests for cancellation checks within agent task logic (using mocked context/job).
    *   Document the structure for Specialized Agents.
    *   Document the handoff confirmation flow (agent proposes -> user confirms -> orchestrator transitions). Add Mermaid diagram.
    *   Document the task cancellation mechanism (API -> SAQ abort -> task check).
    *   Update `backend/README.md`, `systemPatterns.md`, `decisionLog.md`.

    ```mermaid
    sequenceDiagram
        participant User
        participant FE as Frontend
        participant API as FastAPI API
        participant SAQW_Agent as SAQ Worker (Agent X)
        participant DB as Database
        participant SAQW_Orch as SAQ Worker (Orchestrator)

        Note over SAQW_Agent: Agent X completes its task (e.g., Research)
        SAQW_Agent->>+DB: update_video_project_state(video_id, status=PENDING_HANDOFF_CONFIRMATION, active_agent_type=AGENT_Y)
        DB-->>-SAQW_Agent: Confirm update
        SAQW_Agent->>FE: Via SSE: "Research complete. Ready for Scripting? (Confirm/Reject)"

        User->>+FE: Clicks "Confirm"
        FE->>+API: POST /chat/{session_id}/message (user_message="Confirm")
        API->>+DB: Get ChatSession, Save Message
        API->>+DB: Get Video state (status=PENDING...)
        DB-->>-API: Return Video state
        API->>+SAQW_Agent: Enqueue run_agent_y_task(..., user_message="Confirm")
        API-->>-FE: 202 Accepted

        Note over SAQW_Agent: Worker picks up Agent Y task
        SAQW_Agent->>DB: Get Video state (status=PENDING...)
        Note over SAQW_Agent: Detects confirmation needed
        SAQW_Agent->>+SAQW_Orch: Enqueue handle_handoff_confirmation(video_id, confirmed=True)
        SAQW_Agent-->>FE: Via SSE: Status: Processing handoff...

        Note over SAQW_Orch: Worker picks up Orchestrator task
        SAQW_Orch->>+DB: update_video_project_state(video_id, status=AGENT_Y_PROCESSING, phase=SCRIPTING)
        DB-->>-SAQW_Orch: Confirm update
        Note over SAQW_Orch: Optionally enqueue initial Agent Y task step if needed
        SAQW_Orch-->>FE: Via SSE: Status: Agent Y starting...
    ```

**Phase 4: Frontend Implementation**

*(Goal: Build the UI for interacting with the multi-agent system via SSE)*

1.  **Integrate SSE Client (`frontend/src/services/sseService.ts` or similar):**
    *   Implement robust SSE client logic using `EventSource` API.
    *   Manage connection per `chat_session_id`. Handle authentication/token passing if needed (e.g., query param, though cookies might work if same-origin).
    *   Parse incoming events based on the defined structure (`type`, `payload`).
    *   Handle errors, reconnections (with backoff), and closing connections when navigating away or switching sessions.
    *   Use a state management solution (React Context, Zustand, etc.) to provide SSE data (messages, status) to components.
2.  **Implement Multi-Session UI Management (`frontend/src/components/SessionManager/`):**
    *   Build UI (using Mantine components) to:
        *   List available sessions (Platform: Assistant, Onboarding; Video: per project). Fetch list via API (`GET /sessions`).
        *   Allow switching between active sessions. Switching should connect/disconnect SSE streams and update the displayed chat context.
        *   Clearly indicate the current session's context (e.g., "Assistant Chat", "Video: My Project - Research Phase").
3.  **Implement Navigation/Dashboard (`frontend/src/pages/DashboardPage.tsx`):**
    *   Create an entry point page after login.
    *   Display list of video projects (fetched via `GET /videos`).
    *   Allow creating new video projects (calling `POST /videos`).
    *   Provide access to platform sessions (Assistant, Onboarding - potentially trigger onboarding check here).
4.  **Update Chat Interface (`frontend/src/pages/ChatPage.tsx`, `components/ChatInput.tsx`, `MessageList.tsx`):**
    *   Connect `ChatInput` to send messages via `POST /chat/{chat_session_id}/message`.
    *   `MessageList` should render messages received from the SSE state manager. Differentiate user vs. agent messages.
    *   Display clear visual indicators for background task status based on SSE `status` events (e.g., "Assistant is thinking...", "Research Agent is running...", "Handoff pending confirmation...").
    *   Implement UI element (e.g., Cancel button, perhaps near status indicator) linked to the task cancellation API (`POST /videos/{video_id}/cancel`). Provide feedback on cancellation attempt (success/failure).
5.  **Testing & Documentation (Phase 4):**
    *   Frontend unit tests (`Vitest`) for components (SessionManager, ChatInput, MessageList, SSE service/hook). Mock SSE events.
    *   Document frontend architecture (state management, routing, component structure).
    *   Document SSE client implementation and event handling.
    *   Document multi-session UI management logic.
    *   Update `frontend/README.md`.

**Phase 5: Integration, Refinement & Final Documentation**

*(Goal: Ensure all parts work together, refine based on testing, finalize docs)*

1.  **Integration Testing:** Perform comprehensive end-to-end testing of the implemented MVP flows:
    *   User onboarding flow.
    *   Assistant interaction (including triggering video creation).
    *   Video session interaction (placeholder agents, status updates).
    *   SSE message and status propagation.
    *   Task cancellation flow.
    *   Session switching.
2.  **Refinement:** Address bugs, performance issues, and usability concerns identified during testing. Refine agent prompts and tool interactions based on results.
3.  **Final Documentation Review:** Ensure all documentation is complete, accurate, and up-to-date:
    *   Root `README.md`.
    *   `backend/README.md`, `frontend/README.md`.
    *   Memory Bank files (`productContext.md`, `activeContext.md`, `decisionLog.md`, `progress.md`, `systemPatterns.md`). Update with final decisions and implementation details.
    *   Code comments and docstrings.
    *   Architectural diagrams (DB, sequence flows).

**C. Cross-Cutting Considerations (Apply throughout)**

*   **SQLAlchemy 2.0+ & Async:** Maintain consistency in DB interactions. Use async sessions/engines.
*   **Modularity & SOLID:** Design components (API endpoints, SAQ tasks, tools, UI components) with clear responsibilities.
*   **Configuration:** Use Pydantic settings (`backend/app/config.py`) loaded from environment variables. Update `.env.example`.
*   **Error Handling:** Implement robust error handling in API, SAQ tasks, and frontend. Log errors (Sentry integration planned). Publish user-facing errors via SSE.
*   **Security:** Protect API endpoints (SuperTokens session verification). Validate all inputs (Pydantic). Ensure SSE connections are authorized. Prevent prompt injection.
*   **Task Persistence:** Ensure SAQ tasks are designed to be restartable/idempotent where possible. Rely on SAQ's persistence via Redis.
*   **Logging:** Implement structured logging throughout the backend.

**D. UI/UX Considerations (To Address During Frontend Implementation)**

*   Clear visual distinction between Platform (Assistant/Onboarding) and Video sessions.
*   Intuitive navigation for accessing sessions and video projects.
*   Non-intrusive but clear real-time feedback on background agent/task status.
*   Clear confirmation dialogues and feedback for actions like task cancellation.
*   Consider accessibility standards.
