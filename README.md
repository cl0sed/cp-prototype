# AI Video Creation Platform - Project README

*(As of: April 22, 2025)*

This README provides a central hub for understanding the project's goals, structure, architecture, development workflow, and current status. It aims to be a self-contained context source for team members and AI agents working on the project.

## 1. High-Level Overview

This project is an AI-powered platform designed to drastically reduce pre-production time (aiming for 90% reduction) for educational content creators by automating research, structuring, and scripting while preserving the creator's unique voice and teaching style. It addresses critical bottlenecks that lead to creator burnout and limit sustainable channel growth.

The primary user interaction model is **conversational, driven by a multi-agent system**. Different AI agents (Platform Agents like Assistant/Onboarding, and specialized Video Agents for tasks like research/scripting) interact with the user within distinct chat sessions. These agents, orchestrated via the Haystack framework (v2+) running as background tasks, guide creators through a human-in-the-loop pre-production pipeline, managed by a dedicated workflow component. Real-time communication is handled via Server-Sent Events (SSE).

## 2. Problem Space & Target Audience

* **Problem:** Educational creators invest significant time (10-30 hours/video) in pre-production, with research/scripting being the major bottleneck (60-70%). This limits output, creates stress, and risks burnout. Existing AI tools often lack the ability to maintain the creator's unique voice and teaching style, a critical factor for audience connection.
* **Primary Target Audience:** "Accelerating Creators" - typically solo creators with 25K-50K subscribers, generating $30K-$75K annually. They are transitioning from passion projects to businesses, feeling the conflict between creative goals and scaling demands, and are highly receptive to solutions that save time while preserving authenticity.
* **Key Pain Points:** Time-Quality Paradox (scaling vs. quality), Creator Burnout, Voice & Authenticity Concerns with AI, Structuring complex educational content effectively.

## 3. Vision & Core Features

* **Vision:** To be the essential pre-production partner for educational creators, enabling them to "Create more without burnout - reclaim your creative passion".
* **Core Value Proposition:**
    * **Time Reduction:** Transform 15-30 hours of research/scripting into 2-3 hours of focused effort.
    * **Voice Preservation ("Creator DNA"):** Analyze existing content to capture and replicate unique linguistic patterns, terminology, pacing, and teaching style, avoiding generic AI output.
    * **Sustainable Scaling:** Allow creators to potentially double content output without increasing stress.
    * **Educational Effectiveness:** Help optimize content structure and clarity for better learning outcomes and viewer retention.
* **Key Feature Modules & Phased Rollout:** (Implementation maps to agents)
    * **Module 1: Creator Voice & Identity:** Creator DNA System, Personal Stories DB (Post-MVP).
    * **Module 2: Strategic Content Intelligence:** Idea Validation (MVP), Knowledge Gap Detector (Post-MVP).
    * **Module 3: Research & Knowledge Management:** Deep Research Automation (PoC/MVP), Factual Verification (PoC/MVP), Audience Research (PoC/MVP).
    * **Module 4: Content Production Pipeline:** Structure Optimization (PoC/MVP), Script Coherence (PoC/MVP), Concept Simplification (PoC/MVP), Hook Development (PoC/MVP), Script Generation (PoC/MVP), Content Safety (PoC/MVP).
    * **Module 5: Content Distribution & Monetization:** Repurposing, Monetization Strategy (Post-MVP).
    * **Module 6: Creator Workflow System:** Streaming Save/Versioning (PoC basic save, MVP simplified versioning), Feedback System (PoC/MVP).
    * **Module 7: Platform Foundation:** Processing Infra, Data Security (PoC/MVP).

## 4. Roadmap & Current Status

* **Phased Approach:** PoC -> Early MVP -> MVP -> Post-MVP.
* **Current Phase:** Post-PoC / Pre-MVP Planning.
    * **PoC Goal:** Validate core research-to-script flow via conversational agent. Establish core architecture. (Completed)
    * **PoC Deliverables:** Basic DNA capture, basic research/verification, basic script generation, minimal UI. (Achieved)
* **Next Phases:**
    * **Early MVP:** Cloud deployment, CI/CD, basic observability (logging, Sentry). Implement foundational multi-agent architecture (Platform Agents, core workflow, SSE, basic memory).
    * **MVP:** Reliable core value prop (initial Video Agent implementations - e.g., Research/Scripting), enhanced AI quality, improved usability (multi-session UI), full observability integration, initial customer readiness, real-time updates via SSE. Task cancellation, basic handoff confirmation.
* **Remaining Decisions / Active Design Areas:** Specific PaaS/DB/Redis provider selection, detailed data ingestion pipelines (post-MVP?), specific Haystack pipeline implementations for Video Agents, detailed observability config (dashboards/alerts), advanced caching, **Workflow Orchestration Strategy (Post-MVP - refine beyond basic SAQ tasks/logic)**, advanced memory implementation (Episodic analysis, Procedural updates).

## 5. Project Structure (Monorepo)

This project uses a monorepo to manage the frontend, backend, and configurations together. The structure has been updated to support the multi-agent architecture:

```plaintext
cp-prototype/
├── .github/                  # CI/CD Automation
│   └── workflows/
│       └── ...
├── .gitignore
├── docker-compose.yml        # Local development environment setup
├── .env.example              # Example env vars for LOCAL development
├── .env.staging.example      # Example env vars for STAGING environment
├── .env.production.example   # Example env vars for PRODUCTION (excluding secrets!)
├── README.md                 # UPDATED: This file
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app definition, middleware, lifespan events (SSE setup?)
│   │   ├── config.py         # Pydantic settings loading from ENV variables
│   │   ├── logging_config.py # Configure application logging
│   │   │
│   │   ├── api/              # FastAPI specifics
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py # Auth checks, DB sessions, Get project state/active agent?
│   │   │   ├── middleware/   # Custom middleware (if needed)
│   │   │   ├── routers/      # Endpoint definitions
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── chat.py       # Handles message ingress, routes to correct agent task based on session
│   │   │   │   ├── sse.py        # NEW: Manages SSE connections/streams per session
│   │   │   │   ├── video.py      # NEW: Endpoints for creating/managing video projects
│   │   │   │   ├── tasks.py      # NEW: Endpoint(s) for task management (e.g., cancellation)
│   │   │   │   ├── user.py
│   │   │   │   └── health.py
│   │   │   └── schemas.py    # API request/response data shapes (Pydantic)
│   │   │
│   │   ├── worker/           # SAQ Worker specifics
│   │   │   ├── __init__.py
│   │   │   ├── settings.py   # SAQ Queue definition, task discovery (imports tasks), cron schedule definitions
│   │   │   └── tasks/        # NEW dir: For background tasks NOT agent execution/orchestration
│   │   │       ├── __init__.py
│   │   │       └── analysis.py # E.g., Episodic/Procedural analysis SAQ tasks (placeholders for MVP)
│   │   │
│   │   ├── db/               # Database specifics
│   │   │   ├── __init__.py
│   │   │   ├── models/       # UPDATED: Reflects multi-agent state, memory, sessions
│   │   │   │   ├── __init__.py # Central import for Alembic
│   │   │   │   ├── user.py       # Includes preferences (JSONB), is_onboarded flag, etc.
│   │   │   │   ├── video.py      # Core video project, tracks phase, status, active_agent_type, link to active task?
│   │   │   │   ├── chat_session.py # Links session to user/video/session_type
│   │   │   │   ├── chat_message.py
│   │   │   │   ├── memory_analyzed_episode.py  # Basic model for future use
│   │   │   │   └── memory_procedural_instruction.py # Basic model for future use
│   │   │   │   # (Video Artifacts stored in Video model JSONB or generic table for MVP)
│   │   │   ├── migrations/   # Alembic DB schema change scripts
│   │   │   └── session.py    # DB connection/session logic
│   │   │
│   │   ├── shared/           # Code shared across backend
│   │   │   ├── __init__.py
│   │   │   ├── clients/      # Clients for 3rd party APIs (if any)
│   │   │   ├── constants/    # Shared Enums (e.g., VideoPhase, VideoStatus, SessionType, AgentType), constants
│   │   │   ├── exceptions/   # Custom error classes
│   │   │   ├── schemas/      # Core internal data shapes (Pydantic)
│   │   │   ├── prompts/      # Shared prompt templates {name}/{version}.j2
│   │   │   └── tools/        # Shared tools (Python functions)
│   │   │       ├── __init__.py
│   │   │       ├── memory.py     # NEW: Shared tools for memory access (history, preferences, artifacts, context)
│   │   │       └── utils.py      # Other shared utility tools (e.g., text processing)
│   │   │
│   │   ├── agents/           # NEW: Contains interactive agents' implementation
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── platform/     # NEW NAME: Agents operating at user/platform level
│   │   │   │   ├── __init__.py
│   │   │   │   ├── assistant/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── pipeline.py # Haystack pipeline definition
│   │   │   │   │   ├── prompts/    # Agent-specific prompts {name}/{version}.j2
│   │   │   │   │   ├── tools.py    # Agent-specific tools
│   │   │   │   │   └── tasks.py    # SAQ task(s) executing the pipeline
│   │   │   │   └── onboarding/
│   │   │   │       └── ... (similar structure)
│   │   │   │
│   │   │   └── video/        # NEW NAME: Agents operating within a specific video context
│   │   │       ├── __init__.py # Imports specific agents?
│   │   │       ├── research/ # Example - Implementation deferred
│   │   │       │   └── ... (pipeline.py, prompts/, tools.py, tasks.py)
│   │   │       └── scripting/ # Example - Implementation deferred
│   │   │           └── ... (pipeline.py, prompts/, tools.py, tasks.py)
│   │   │       # ... (Other video-specific agents added here later)
│   │   │
│   │   └── workflow/         # NEW: Module dedicated to workflow management logic
│   │       ├── __init__.py
│   │       └── orchestrator/ # Contains Orchestrator logic/tasks
│   │           ├── __init__.py
│   │           ├── logic.py    # Core state machine/transition rules?
│   │           └── tasks.py    # SAQ task(s) implementing orchestration
│   │
│   ├── tests/                # UPDATED: Mirror new app structure (agents/, workflow/, etc.)
│   │   └── ...
│   │
│   ├── Dockerfile            # Builds the common backend image (API + Worker code)
│   ├── pyproject.toml        # Python dependencies
│   ├── alembic.ini           # Alembic configuration file
│   ├── ruff.toml             # Linter/Formatter config
│   └── README.md             # UPDATED: Backend setup, running locally, migration cmd, testing cmd
│
├── frontend/                 # React structure (Needs SSE client, multi-session UI management)
│   └── ...                   # See frontend/README.md for details
│
├── e2e_tests/                # End-to-end tests
│   └── .gitkeep
│
├── infra/                    # Optional: Infrastructure-as-Code
│   └── .gitkeep
│
└── scripts/                  # Optional: Helper scripts
    └── .gitkeep
```

* **`backend/`:** Python API (FastAPI) & Background Task Worker (SAQ). See `backend/README.md`.
* **`frontend/`:** React User Interface. See `frontend/README.md`.
* **Root:** Shared configurations, local development setup (`docker-compose.yml`), CI/CD workflows.

## 6. Architecture

Architecture choices prioritize developer velocity, low operational overhead ("Low-Ops"), cost-efficient scaling, and creator voice authenticity. The architecture is designed around a **multi-agent system** interacting with the user via distinct conversational sessions.

### 6.a. Core Technology Stack

* Backend Language/Framework: Python / FastAPI
* AI Orchestration: Haystack Framework (v2+)
* Frontend Framework: React
* Database: Managed PostgreSQL / `pgvector` extension
* DB Migrations: Alembic
* Background Tasks: SAQ library
* Task Queue Broker: Managed Redis
* Real-time Communication: **Server-Sent Events (SSE)**
* Authentication: SuperTokens (Managed Service)
* Hosting: Container-based PaaS

### 6.b. Guiding Principles

* Minimize direct infrastructure operation ("Low-Ops").
* Minimize vendor lock-in.
* Prioritize creator voice authenticity.
* Async-first design.
* Modularity & Rapid Iteration (supported by multi-agent structure).
* Design for Idempotency (especially background tasks).

### 6.c. Key Patterns

* Async-first design.
* Dependency Injection (FastAPI).
* Single Backend Docker Image (API + Worker code).
* **Multi-Agent Conversational System:** Core interaction pattern using Platform and Video agents.
* **Distributed Workflow Orchestration:** Using SAQ tasks and dedicated logic (`workflow/orchestrator/`) to manage state transitions between agents.
* **Contextual Memory Management:** Utilizing different strategies (Working, Episodic, Semantic, Procedural) accessed via standardized tools.

### 6.d. API / Worker / Agent Design Strategy (Updated)

* **API (FastAPI):** Handles synchronous requests (auth, validation), initiates workflows by enqueueing the first relevant agent task, manages SSE connections, handles task management requests (e.g., cancellation). Responsible for routing incoming chat messages to the correct active agent's task based on session context.
* **Worker (SAQ):** Executes all long-running, I/O-bound, or complex logic as background tasks. This includes:
    * Executing Haystack pipelines for Platform and Video agents.
    * Running Orchestrator tasks for workflow management (state transitions, handoffs).
    * Performing background memory analysis/update tasks (post-MVP).
* **Agents (Haystack Pipelines within SAQ Tasks):** Encapsulate conversational logic, LLM interaction, and tool use for specific contexts (Platform or Video). They read from and write to memory/state via shared tools and publish results/status via SSE.
* **Orchestrator (Python Logic within SAQ Tasks):** Manages the state transitions between agent phases based on defined rules, agent completion signals, and user confirmations.
* **Communication Flow (MVP):**
    1.  User interacts via Frontend.
    2.  Frontend sends request (HTTP POST) to API with `session_id`.
    3.  API validates, identifies context (user/video/active\_agent), saves user message, enqueues the appropriate agent's SAQ task.
    4.  API maintains an open SSE connection for that `session_id`.
    5.  SAQ task executes agent pipeline -> interacts with DB/Memory Tools -> generates response/status updates.
    6.  SAQ task publishes messages/status updates to the SSE stream via helper/Redis.
    7.  Frontend receives SSE events and updates UI in real-time.
    8.  Agent task completes, potentially updating project state, triggering Orchestrator task if phase transition is needed.

### 6.e. Data Layer Details (Updated)

* Schema supports multi-agent state (`Video.active_agent_type`, `Video.phase`, `Video.status`), distinct session types (`ChatSession.session_type`), and foundational memory structures (`User.preferences`, basic `AnalyzedEpisode`, `ProceduralInstruction`).
* Video artifacts stored structurally (JSONB or generic table) linked to `Video` model for MVP.
* Vector Data (`pgvector`): Used for Semantic Memory (RAG) and potentially future Episodic Memory search.

### 6.f. Architecture Considerations & Technical Debt

* **Workflow Orchestration:** Basic orchestration via SAQ tasks and DB state is suitable for MVP. Complex, multi-step, branching workflows with robust error handling remain **deferred technical debt**, likely requiring a dedicated engine (Temporal, Prefect) Post-MVP. The `workflow/` module provides a place for this future integration.
* **Memory Management:** MVP implements basic memory handling. Advanced analysis (Episodic) and automated updates (Procedural) are deferred.
* **Rollback Implementation:** The logic for actually performing rollbacks (including data handling) is deferred.

### 6.g. Observability Strategy (MVP Target)

* Instrumentation: OpenTelemetry SDK. Platforms: Grafana Cloud (Logs, Metrics, Traces), Sentry (Errors, APM), PostHog (Product Analytics).

### 6.h. Prompt and Tool Versioning (Updated Paths)

* Prompt templates (`.j2`) stored under agent-specific directories: `backend/app/agents/platform/.../prompts/` or `backend/app/agents/video/.../prompts/`. Shared prompts remain in `backend/app/shared/prompts/`.
* Tool definitions (`.py`) stored agent-specifically (`agents/.../tools.py`) or shared (`shared/tools/*.py`, including `shared/tools/memory.py`).
* Activation via pipeline tags, configuration (`pipeline-tags.yaml`), `PromptService`, fallback, and startup validation remains conceptually the same. Paths used by `PromptService` need updating.

### 6.i. Detailed Architecture Overview (Updated Conceptual Flow)

The system uses a multi-agent architecture orchestrated via background tasks and real-time events.

1.  **Frontend (React):** Manages multiple chat sessions (Platform, Video contexts), interacts with the API via HTTP POST for actions/messages, maintains persistent SSE connections per session for receiving real-time updates (messages, status), displays task progress and cancellation options.
2.  **Backend API (FastAPI):** Authenticates requests, handles session context lookup, routes incoming messages to the correct agent's SAQ task, manages SSE connections, provides endpoints for video/task management.
3.  **Backend Worker (SAQ):** Executes all agent pipelines (Haystack) and workflow logic (Orchestrator) as background tasks. Communicates results/status back via SSE publishing mechanism (e.g., Redis Pub/Sub). Executes scheduled analysis tasks.
4.  **Agents (Haystack Pipelines in SAQ tasks):** Handle specific conversational contexts (Platform or Video). Use shared tools to interact with memory (Working, Semantic, Project Context). Generate responses and status updates.
5.  **Workflow/Orchestrator (Python Logic in SAQ tasks):** Manages state transitions between video phases based on agent signals and user confirmations. Handles rollback logic placeholders.
6.  **Database (PostgreSQL + pgvector):** Stores all state (user, video project, session), chat history, memory components (preferences, artifacts, future episodic/procedural data), vector embeddings.
7.  **Redis:** Acts as the SAQ broker and likely the Pub/Sub mechanism for SSE event distribution.
8.  **External Services:** SuperTokens (Auth), LLMs (via Haystack).

#### Architectural Diagram (Conceptual Update):

```mermaid
graph TD
    User --> Nginx
    Nginx --> Frontend
    Nginx --> BackendAPI

    subgraph Frontend[User Interface (React)]
        direction LR
        UI_Sessions[Multi-Session UI]
        UI_Chat[Chat Interface]
        SSE_Client[SSE Client]
        API_Client[API Client (HTTP)]
    end

    subgraph Backend
        direction TB
        BackendAPI[Backend API (FastAPI)]
        subgraph Worker[Async Worker (SAQ)]
            direction LR
            Agent_Platform[Platform Agents (Haystack)]
            Agent_Video[Video Agents (Haystack)]
            Workflow_Orchestrator[Orchestrator (Python)]
            Background_Tasks[Other Tasks (e.g., Analysis)]
        end
        subgraph DataStores[Data Stores]
           PostgreSQL[PostgreSQL + pgvector]
           Redis[Redis (SAQ Broker + Pub/Sub)]
        end
    end

    subgraph ExternalServices[External Services]
        SuperTokensMS[SuperTokens Managed Service]
        ExternalLLMs[External LLMs]
    end

    Frontend -- HTTP Requests --> BackendAPI
    BackendAPI -- SSE Connection Mgmt --> Frontend
    BackendAPI -- Enqueue Task --> Redis
    BackendAPI -- Read/Write State --> PostgreSQL
    BackendAPI -- Auth Calls --> SuperTokensMS

    Worker -- Poll Tasks --> Redis
    Worker -- Publish Events --> Redis
    Redis -- Push Events via Helper? --> BackendAPI # Mechanism for SSE push needed
    Worker -- Read/Write State/Data --> PostgreSQL
    Agent_Platform -- Uses --> ExternalLLMs
    Agent_Video -- Uses --> ExternalLLMs

    classDef component fill:#ccf,stroke:#333,stroke-width:2px;
    classDef datastore fill:#cfc,stroke:#333,stroke-width:2px;
    classDef external fill:#ffc,stroke:#333,stroke-width:2px;
    classDef workerproc fill:#f9f,stroke:#333,stroke-width:2px;


    class Frontend,BackendAPI,Nginx component;
    class PostgreSQL,Redis datastore;
    class SuperTokensMS,ExternalLLMs external;
    class Worker,Agent_Platform,Agent_Video,Workflow_Orchestrator,Background_Tasks workerproc

    linkStyle default stroke:#555,stroke-width:1.5px,color:#555;

```
*(Note: Mermaid diagram simplified to show key components and interactions in the new architecture).*

## 7. Development Workflow

(Details on Setup, Running Locally, Migrations, Testing Commands, Linters/Formatters should be maintained and updated in `backend/README.md` and `frontend/README.md` based on the new structure).
