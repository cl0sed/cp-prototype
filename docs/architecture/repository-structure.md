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
├── README.md                 # UPDATED: High-level overview, Arch decisions, Setup, How to Run
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
│   │   │   │   ├── video.py      # NEW: Endpoints for creating/managing video projects, potentially cancellation
│   │   │   │   ├── user.py
│   │   │   │   └── health.py
│   │   │   └── schemas.py    # API request/response data shapes (Pydantic)
│   │   │
│   │   ├── worker/           # SAQ Worker specifics
│   │   │   ├── __init__.py
│   │   │   ├── settings.py   # SAQ Queue definition, task discovery (imports tasks), cron schedule definitions
│   │   │   └── tasks/        # NEW dir: For background tasks NOT agent execution/orchestration
│   │   │       ├── __init__.py
│   │   │       └── analysis.py # E.g., Episodic/Procedural analysis SAQ tasks
│   │   │
│   │   ├── db/               # Database specifics
│   │   │   ├── __init__.py
│   │   │   ├── models/       # UPDATED: Add models for artifacts, state, memory schemas
│   │   │   │   ├── __init__.py # Central import for Alembic
│   │   │   │   ├── user.py       # Includes preferences, is_onboarded flag, etc.
│   │   │   │   ├── video.py      # Core video project, tracks phase, status, active_agent
│   │   │   │   ├── chat_session.py # Links session to user/video/agent-type
│   │   │   │   ├── chat_message.py
│   │   │   │   ├── creator_dna_profile.py # Example structured semantic data
│   │   │   │   ├── video_artifact_structure.py # Example artifact model
│   │   │   │   ├── video_artifact_topics.py    # Example artifact model
│   │   │   │   ├── memory_analyzed_episode.py  # Example episodic memory model
│   │   │   │   └── memory_procedural_instruction.py # Example procedural memory model
│   │   │   ├── migrations/   # Alembic DB schema change scripts
│   │   │   │   └── ...
│   │   │   └── session.py    # DB connection/session logic
│   │   │
│   │   ├── shared/           # Code shared across backend
│   │   │   ├── __init__.py
│   │   │   ├── clients/      # Clients for 3rd party APIs (if any)
│   │   │   ├── constants/    # Shared Enums, constants
│   │   │   ├── exceptions/   # Custom error classes
│   │   │   ├── schemas/      # Core internal data shapes (distinct from API/DB)
│   │   │   ├── prompts/      # Shared prompt templates (e.g., error handling prompts?)
│   │   │   │   └── {name}/{version}.j2
│   │   │   └── tools/        # Shared tools (Python functions)
│   │   │       ├── __init__.py
│   │   │       ├── memory.py     # NEW: Shared tools for memory access (get_history, retrieve_episodic, retrieve_semantic, get_artifact_X)
│   │   │       └── utils.py      # Other shared utility tools (e.g., text processing)
│   │   │
│   │   ├── agents/           # UPDATED: Now only contains interactive agents
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── platform/     # NEW NAME: Agents operating at user/platform level
│   │   │   │   ├── __init__.py
│   │   │   │   ├── assistant/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── pipeline.py # Haystack pipeline definition
│   │   │   │   │   ├── prompts/    # Agent-specific prompts {name}/{version}.j2
│   │   │   │   │   ├── tools.py    # Agent-specific tools (if any beyond shared)
│   │   │   │   │   └── tasks.py    # SAQ task(s) executing the pipeline
│   │   │   │   └── onboarding/
│   │   │   │       └── ... (similar structure)
│   │   │   │
│   │   │   └── video/        # NEW NAME: Agents operating within a specific video context
│   │   │       ├── __init__.py # Imports specific agents?
│   │   │       ├── research/ # Example - To be implemented later
│   │   │       │   └── ... (pipeline.py, prompts/, tools.py, tasks.py)
│   │   │       └── scripting/ # Example - To be implemented later
│   │   │           └── ... (pipeline.py, prompts/, tools.py, tasks.py)
│   │   │       # ... (Other video-specific agents added here as needed)
│   │   │
│   │   └── workflow/         # NEW: Module dedicated to workflow management
│   │       ├── __init__.py
│   │       └── orchestrator/ # MOVED & RENAMED: Orchestrator logic/tasks
│   │           ├── __init__.py
│   │           ├── logic.py    # Core state machine/transition rules?
│   │           └── tasks.py    # SAQ task(s) implementing orchestration
│   │
│   ├── tests/                # UPDATED: Mirror new app structure (agents/, workflow/, etc.)
│   │   ├── __init__.py
│   │   └── ...
│   │
│   ├── Dockerfile            # Builds the common backend image (API + Worker code)
│   ├── pyproject.toml        # Python dependencies
│   ├── alembic.ini           # Alembic configuration file
│   ├── ruff.toml             # Linter/Formatter config
│   └── README.md             # UPDATED: Backend setup, running locally, migration cmd, testing cmd
│
├── frontend/                 # React structure (Needs SSE client, multi-session UI management)
│   ├── src/
│   │   ├── services/         # UPDATED: apiService.ts needs SSE client logic integration
│   │   ├── contexts/         # UPDATED: Potentially context for managing active session / multiple sessions
│   │   ├── components/       # UPDATED: UI components for switching sessions, indicating task status/cancellation
│   │   └── ...
│   ├── ...
│   └── README.md             # Needs updating for SSE handling, multi-session UI
│
├── e2e_tests/                # End-to-end tests (Playwright/Cypress)
│   └── .gitkeep
│
├── infra/                    # Optional: Infrastructure-as-Code (Terraform, Pulumi)
│   └── .gitkeep
│
└── scripts/                  # Optional: Helper scripts
    └── .gitkeep
```
