# Haystack 2.0 Chat Refactor Plan

This plan outlines the steps to replace Portkey with standard Haystack 2.0 components, implement prompt/pipeline versioning, add necessary database models, create new consolidated chat API endpoints, implement function calling, and update the frontend.

**Phase 1: Prerequisites & Setup**

1.  **Database Model Updates (`backend/app/db/models.py`):**
    *   **[F3]** Add `role: Mapped[str]` to the `User` model (e.g., default 'user'). Consider using an `Enum` for roles.
    *   **[F1]** Define `PromptTemplate` model (`id`, `name`, `version`, `template_type`, `content`, `metadata`, `created_at`, `updated_at`). Add `UniqueConstraint("name", "version")`.
    *   **[F2]** Define `ChatMessage` model (`id`, `user_id` FK, `session_id` UUID/String, `role` Enum/String, `content` Text, `timestamp`, `metadata` JSONB).
    *   **[F2]** Add crucial indexes to `ChatMessage`:
        *   `Index("ix_chat_message_session_timestamp", "session_id", "timestamp")`
        *   `Index("ix_chat_message_user_timestamp", "user_id", "timestamp")`
    *   **[F5]** Generate Alembic migration script (`alembic revision --autogenerate -m "Add chat models, user role, prompt templates"`). Review script carefully, ensuring indexes are included. Apply migration (`alembic upgrade head`).

2.  **Configuration (`backend/app/config.py`, `prompts.yaml`, `.env.example`):**
    *   **[F1, F4]** Define `prompts.yaml` structure (example below). Create `prompts.yaml.example`.
        ```yaml
        # prompts.yaml.example
        # Maps pipeline steps/tags to specific prompt template versions
        pipelines:
          chat_v1:
            greeting_prompt:
              name: "chat_greeting"
              version: "1.0"
            main_prompt:
              name: "chat_main"
              version: "1.0"
        # Add more pipelines/steps as needed
        ```
    *   **[F4]** Define standard ENV VAR name for pipeline version selection, e.g., `CHAT_PIPELINE_TAG="chat_v1"`. Add to `.env.example`.
    *   **[F1, F4, F5]** Update `config.py` (Pydantic settings) to:
        *   Load `CHAT_PIPELINE_TAG`.
        *   Load the OpenAI API key (`OPENAI_API_KEY`) - remove Portkey keys.
        *   Include a function/method to load and parse `prompts.yaml`.
    *   **[F5]** Remove Portkey-related ENV VARs (`PORTKEY_API_KEY`, `PORTKEY_CHAT_VIRTUAL_KEY`) from `.env.example`.

**Phase 2: Backend Implementation (FastAPI)**

1.  **Core Services (`backend/app/services/`, `backend/app/ai/`):**
    *   **[F1, F4]** Implement `PromptService` (`backend/app/services/prompt_service.py`):
        *   Reads prompt config from `settings`.
        *   Fetches specific `PromptTemplate.content` from DB based on name+version provided by config for a given pipeline tag/step.
    *   **[F4, F2, F3]** Implement Pipeline Builder(s) (`backend/app/ai/pipeline_builder.py`):
        *   Create function(s) like `build_chat_pipeline(pipeline_tag: str, prompt_service: PromptService) -> AsyncPipeline`.
        *   Read `pipeline_tag` (from settings).
        *   Use `PromptService` to get correct prompt template content based on tag.
        *   Construct Haystack `AsyncPipeline` programmatically:
            *   `PromptBuilder`: Use fetched template string. Template should accept `chat_history` (list of `ChatMessage`), `user` (object with `id`, `role`), `session_id`, etc.
            *   `OpenAIChatGenerator`: Configure with `settings.OPENAI_API_KEY`, desired model.
            *   `Tool`s: Define `get_current_time`, `get_user_tasks` (see step 2).
            *   `Agent`: Integrate the generator and tools. Configure `system_prompt` (potentially fetched via `PromptService`), `exit_conditions`.
    *   **[F5]** Refactor `ChatService` (`backend/app/services/chat_service.py`):
        *   Remove dependency on old `build_chat_pipeline`.
        *   Inject `PromptService`.
        *   Call new `build_chat_pipeline` with `settings.CHAT_PIPELINE_TAG`.
        *   Modify `interact` method:
            *   Accept `session_id`.
            *   Store incoming user message in `ChatMessage` table (using DB session).
            *   Fetch recent `ChatMessage` history based on `session_id` (using index).
            *   Format history correctly for `PromptBuilder`.
            *   Run the new pipeline, passing `chat_history`, `user` object, `session_id` as input to the `Agent`.
            *   Store assistant/tool responses in `ChatMessage` table.
            *   Return assistant's final reply and `session_id`.
    *   **[F5]** Remove `backend/app/ai/portkey_generator.py` and update imports.

2.  **Tool Definitions (`backend/app/ai/tools.py`):**
    *   **[F3]** Implement `get_current_time` as a Haystack `Tool`.
    *   **[F3]** Implement `get_user_tasks` as a Haystack `Tool`:
        *   Accept `user` object (containing `id` and `role`) from Agent's state/input.
        *   Perform role check (e.g., only 'admin' can see all tasks).
        *   Query database (e.g., `Project` or a dedicated `Task` table if it exists) based on `user_id` and role.
        *   Return formatted task list.

3.  **API Endpoints (`backend/app/api/routers/chat.py`):**
    *   **[F2]** Create new router file `backend/app/api/routers/chat.py`.
    *   **[F2]** `GET /api/chat/greeting`:
        *   Depends on `get_required_user_from_session`.
        *   Inject `ChatService` (or potentially a dedicated GreetingService).
        *   Fetch user-specific info (e.g., recent tasks via `get_user_tasks` logic or direct query).
        *   Use a dedicated greeting prompt/pipeline (configured in `prompts.yaml`) to generate a dynamic greeting.
    *   **[F2]** `GET /api/chat/history`:
        *   Depends on `get_required_user_from_session`.
        *   Accept optional `session_id` (UUID/str) and `limit` (int) query parameters.
        *   Query `ChatMessage` table using `user_id` and optionally `session_id` (leveraging indexes). Order by `timestamp`. Apply `limit`.
        *   Return list of messages.
    *   **[F2, F3, F4]** `POST /api/chat/message`:
        *   Depends on `get_required_user_from_session`.
        *   Inject `ChatService`.
        *   Define request body model (e.g., `ChatMessageRequest`) expecting `message: str` and optional `session_id: Optional[UUID]`.
        *   Define response body model (e.g., `ChatMessageResponse`) returning `reply: str` and `session_id: UUID`.
        *   If `session_id` is missing/null, generate a new one (`uuid.uuid4()`).
        *   Call `chat_service.interact`, passing user message, (empty history if new session), user object, and the `session_id`.
        *   Return the agent's reply and the (potentially new) `session_id`.
    *   **[F5]** Register the new `chat.py` router in `backend/app/main.py`.
    *   **[F5]** Remove or comment out the old `/agent/interact` endpoint in `backend/app/api/routers/agent.py`.

4.  **Data Seeding (Optional - `backend/app/db/seed.py` or Alembic migration):**
    *   **[F1]** Create script/migration to insert initial `PromptTemplate` rows into the database.

**Phase 3: Frontend Implementation (React)**

*(High-level steps for Code mode)*
1.  **[F2]** Update main Chat UI component (`ChatPage.tsx`):
    *   Manage state: `messages` (array), `currentInput`, `isLoading`, `greeting`, `sessionId` (string/null).
2.  **[F2]** API Integration (`apiService.ts`, `ChatPage.tsx`):
    *   On load (`useEffect`):
        *   Call `GET /api/chat/greeting` -> update `greeting` state.
        *   Check local storage for `sessionId`.
        *   If `sessionId` exists, call `GET /api/chat/history?session_id={sessionId}` -> update `messages` state.
        *   If no `sessionId`, potentially call `GET /api/chat/history` (without session) to show recent conversations list (optional enhancement).
    *   On message send:
        *   Set `isLoading` true.
        *   Add user message to `messages` state immediately.
        *   Call `POST /api/chat/message` with `{ message: currentInput, session_id: sessionId }`.
        *   On response:
            *   Update `sessionId` state (and store in local storage) from response.
            *   Add assistant reply to `messages` state.
            *   Set `isLoading` false.
3.  **[F2]** Rendering: Display greeting, message list, input field, loading indicator, handle errors.
4.  **[F5]** Ensure adherence to React 19.1, Mantine, TypeScript practices.

**Phase 4: Testing**

*(High-level steps for Test mode)*
1.  **Backend (pytest):**
    *   Unit tests for `PromptService` (mock DB).
    *   Unit tests for pipeline builder(s) (mock services/components).
    *   Unit tests for `get_current_time`, `get_user_tasks` (mock DB, verify role checks).
    *   Integration tests for `/api/chat` endpoints (mock `ChatService` or use test DB/pipeline). Verify `session_id` handling, history retrieval (check query plans if possible to confirm index usage), auth.
    *   Test DB models and Alembic migration (ensure indexes are created).
2.  **Frontend (Vitest/Playwright):**
    *   Unit tests for `ChatPage` component (mock API calls, test state updates for `sessionId`).
    *   E2E tests for the full chat flow: Send message -> Get greeting -> Send follow-up -> Verify history persistence within session -> Start new session.

**Phase 5: Documentation & Cleanup**

1.  **[F5]** Update `README.md`, `backend/README.md`, `frontend/README.md`.
2.  **[F5]** Update `docs/PATTERNS.txt` (or similar architecture docs).
3.  **[F1, F2, F3]** Document new/updated DB tables (`prompt_templates`, `chat_messages` + indexes, `users.role`) in schema diagrams or markdown.
4.  **[F1, F4]** Document `prompts.yaml` format and the `CHAT_PIPELINE_TAG` ENV VAR.
5.  **[F2, F3]** Document new `/api/chat/*` endpoints (request/response formats, `session_id` handling, auth). Use OpenAPI schema generation.
6.  **[F5]** Update `.env.example` and `prompts.yaml.example`.
7.  **[F5]** Explicitly state Portkey removal and direct Haystack LLM usage in relevant docs.
8.  **[F5]** Update Memory Bank files (`productContext.md`, `activeContext.md`, `progress.md`, `systemPatterns.md`, `decisionLog.md`) to reflect the new architecture, completed tasks, and decisions.

---

**Diagram: Simplified Chat API Flow (`POST /api/chat/message`)**

```mermaid
sequenceDiagram
    participant FE as Frontend (React)
    participant BE_API as Backend API (FastAPI /chat)
    participant BE_SVC as ChatService
    participant DB as Database (PostgreSQL)
    participant BE_PIPE as Haystack Pipeline (Agent)

    FE->>+BE_API: POST /api/chat/message (message, session_id?)
    Note over BE_API: Auth Check (SuperTokens)
    BE_API->>BE_API: Generate new session_id if null
    BE_API->>+BE_SVC: interact(user_msg, user, session_id)
    BE_SVC->>+DB: Store User Message (ChatMessage)
    DB-->>-BE_SVC: Stored OK
    BE_SVC->>+DB: Fetch History (ChatMessage by session_id)
    DB-->>-BE_SVC: Return History
    BE_SVC->>+BE_PIPE: run_async(history, user, session_id, ...)
    Note over BE_PIPE: Agent uses PromptBuilder, LLM, Tools
    BE_PIPE-->>-BE_SVC: Return Agent Reply/Tool Results
    BE_SVC->>+DB: Store Assistant/Tool Messages (ChatMessage)
    DB-->>-BE_SVC: Stored OK
    BE_SVC-->>-BE_API: Return final reply, session_id
    BE_API-->>-FE: Response (reply, session_id)
