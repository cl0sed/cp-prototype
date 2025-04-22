# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.

## Coding Patterns

*   Dependency Injection (via FastAPI). [Source: README.md Sec 6.c]
*   Use SAQ `Status` enum for background task status consistency. [Source: backend/README.md Sec SAQ Limitations]
*   Use SQLAlchemy ORM for database operations within SAQ hooks. [Source: backend/README.md Sec SAQ Limitations]
*   Error Handling: Catch exceptions in SAQ hooks, let SAQ handle task failures (log & re-raise in tasks). [Source: backend/README.md Sec SAQ Limitations]
*   SAQ Usage: Prioritize understanding SAQ patterns, syntax, and implementation by referencing the existing code within the `@/backend/app/worker` directory. For supplementary information, official documentation, or features not demonstrated locally, consult the official SAQ repository: `https://github.com/tobymao/saq/tree/main/saq`.
*   Code Quality: Enforced via pre-commit hooks (Ruff, Black, ESLint, Prettier). [Source: README.md Sec 7]
*   Authentication Overrides: Use SuperTokens API overrides to integrate with our database models, ensuring user data synchronization between SuperTokens and our database. [Source: backend/app/features/auth/supertokens_config.py]
*   React State Management: Use React hooks (useState, useContext, etc.) for state management. [Source: frontend-react/src/contexts/AuthContext.tsx]
*   Custom Haystack Components: Define custom components using the `@component` decorator and subclassing `haystack.core.component.Component` to wrap external libraries or custom logic within the Haystack pipeline framework.
*   Use Cached `Settings` object through `get_settings` instead of accessing the `Settings` directly.
*   Store agent-specific prompts in `agents/platform/.../prompts/{prompt_name}/{version}.j2` or `agents/video/.../prompts/{prompt_name}/{version}.j2`. Shared prompts remain in `shared/prompts/{prompt_name}/{version}.j2`. [Source: README.md Sec 6.h]
*   Store agent-specific tools in `agents/platform/.../tools.py` or `agents/video/.../tools.py`. Shared tools are located in `shared/tools/*.py`, including `shared/tools/memory.py`. [Source: README.md Sec 6.h]
*   Versioning pattern for prompts: `{prompt_name}/{version}.j2` within the respective prompts directory.
*   Prompt and Tool Versioning: Prompts and tools are versioned in Git, activated via pipeline tags (default or override), configured via `pipeline-tags.yaml` with a fallback to `DEFAULT_PROMPT_VERSION`, and managed by `PromptService`. Startup validation ensures config integrity and file existence for default tags.
*   Message Content Access: Use `.text` to access the main textual content of a Haystack `ChatMessage` object. Use `.content` to access the main textual content of a database `ChatMessage` model object. Be mindful of which object type you are working with. [2025-04-21 13:08:50]

*   Logging Standard: Use `logging.getLogger(__name__)` to obtain a named logger instance in each module. Use appropriate logging levels (`debug`, `info`, `warning`, `error`, `critical`, `exception`). Ensure log messages are clear, concise, and do not include the log level in the message text. Use `logger.exception()` to log exceptions with traceback. Avoid `print()` for log output.
*   Comment Standard: Use docstrings for modules, classes, and functions to explain their purpose. Use inline comments sparingly to clarify complex or non-obvious code. Remove unnecessary, redundant, self-explanatory, or excessive comments (including commented-out file paths). Clearly mark temporary or incomplete code with comments like `# TODO` or by commenting out blocks.

## Architectural Patterns

*   Monorepo Structure: Centralized management of frontend, backend, and configs. [Source: README.md Sec 5]
*   Async-first Design: Leveraging async capabilities in FastAPI and SAQ. [Source: README.md Sec 6.b, 6.c]
*   Single Backend Docker Image: Bundles API and Worker for simplified deployment. [Source: README.md Sec 6.c]
*   API/Worker Split: API for synchronous requests & task triggering, Worker for asynchronous/long-running tasks. [Source: README.md Sec 6.d, backend/README.md Sec SAQ]
*   Background Task Queue: Using SAQ library with Redis as the broker. [Source: README.md Sec 6.a, backend/README.md Sec SAQ]
*   Vector Database for RAG: Utilizing PostgreSQL with the `pgvector` extension. [Source: README.md Sec 6.a, 6.e]
*   Database Migrations: Managed via Alembic. [Source: README.md Sec 6.a, 7]
*   Deployment Target: Container-based PaaS. [Source: README.md Sec 6.a]
*   Configuration Management: Primarily via environment variables (local via `.env`, deployed via platform secrets). [Source: README.md Sec 7]
*   Authentication Architecture: Using SuperTokens Managed Service with a two-tier approach - SuperTokens for auth management and our database for user data, linked via `supertokens_user_id`. [Source: backend/app/features/auth/supertokens_config.py]
*   Centralized Base URL Configuration: Using `settings.APP_BASE_URL` from `config.py` for all application URLs (e.g., SuperTokens configuration). [Source: backend/app/features/auth/supertokens_config.py, backend/app/config.py]
*   API Protection: Using SuperTokens session verification as a FastAPI dependency to protect routes. [Source: backend/app/api/routers/agent.py]
*   Required User Dependency: Using `get_required_user_from_session` to ensure a valid user exists for authenticated endpoints. [Source: backend/app/features/auth/supertokens_config.py, backend/app/api/routers/agent.py, backend/app/api/routers/user.py]
*   Docker-Based Development & Deployment: Using Docker Compose for consistent local environments and deployment. [Source: docker-compose.yaml]
*   Atomic Database Models: Organizing SQLAlchemy models into separate, domain-specific files within `backend/app/db/models/` for improved structure and maintainability.
*   Alembic Migration Dependency Resolution: Leveraging Alembic's built-in dependency analysis supplemented by `use_alter=True` on specific foreign keys to handle circular dependencies during schema creation.
*   Programmatic Migration Customization: Utilizing the `alembic.env.py` `process_revision_directives` hook to automatically include necessary database commands (e.g., `CREATE EXTENSION`) in generated migration scripts, avoiding manual editing.
*   Centralized Model Registration: Importing all SQLAlchemy models in `backend/app/db/models/__init__.py` to ensure Alembic's metadata is fully populated for autogenerate.
*   **Multi-Agent Conversational System:** The core interaction pattern is driven by distinct AI agents (Platform and Video agents) interacting with users via separate chat sessions, orchestrated as background tasks. [Source: README.md Sec 1, 6.c, 6.d, 6.i]
*   **Distributed Workflow Orchestration:** SAQ tasks and dedicated workflow logic (`workflow/orchestrator/`) manage state transitions between agents and video phases. A more robust workflow engine is deferred technical debt. [Source: README.md Sec 6.c, 6.d, 6.f, 6.i]
*   **Contextual Memory Management:** Different memory strategies (Working, Episodic, Semantic, Procedural) are utilized and accessed via standardized tools (`shared/tools/memory.py`) to maintain context across agent interactions. Advanced analysis and updates are deferred. [Source: README.md Sec 6.c, 6.f, 6.i, 6.e]
*   **Real-time Communication via Server-Sent Events (SSE):** Used for the backend (API/Worker) to push real-time updates (messages, status, progress) to the frontend, managing persistent connections per user session. [Source: README.md Sec 6.a, 6.d, 6.i]
*   **Comprehensive Observability Strategy:** Implementation targets MVP using OpenTelemetry SDK for instrumentation, with Grafana Cloud (Logs, Metrics, Traces), Sentry (Errors, APM), and PostHog (Product Analytics) as target platforms. [Source: README.md Sec 6.g]

## Frontend Patterns

*   React Version: Using React 19.1 for modern React features and performance improvements. [Source: frontend-react/package.json]
*   Component Library: Using Mantine 7.17.4 (https://mantine.dev/) for UI components to maintain consistent design. [Source: frontend-react/package.json]
*   Styling: Using Mantine's styling system with CSS-in-JS approach. [Source: frontend-react/src/main.tsx]
*   Theming: Centralizing theme configuration using Mantine's createTheme function. [Source: frontend-react/src/main.tsx]
*   Form Handling: Using Mantine Form (useForm) for form state management, validation, and submission. [Source: frontend-react/src/pages/auth/*.tsx]
*   Authentication: Using SuperTokens Auth React SDK directly for authentication flows. [Source: frontend-react/src/config/supertokens.ts]
*   Authentication UI: Custom authentication components built with Mantine UI components. [Source: frontend-react/src/pages/auth/*.tsx]
*   API Client: Using standard fetch-based API service relying on browser cookie handling (`credentials: 'include'`). [Source: frontend-react/src/services/apiService.ts]
*   Protected Routes: Client-side route protection using SuperTokens SessionAuth component. [Source: frontend-react/src/routes/index.tsx]
*   Authentication State: Primarily managed via SuperTokens `useSessionContext` hook. [Source: frontend-react/src/layouts/MainLayout.tsx]
*   Context API: Potentially used for non-auth global state management if needed.
*   TypeScript Integration: Strong typing throughout the application with proper environment variable declarations. [Source: frontend-react/src/vite-env.d.ts]
*   Frontend Component Typing: Use TypeScript interfaces to define props and state for React components, ensuring type safety and improving component usage clarity.

## Testing Patterns

*   Backend Testing: Unit/integration tests using `pytest`. [Source: backend/README.md Sec Testing]
*   Frontend Testing: Framework/details likely in `frontend/README.md`. [Source: README.md Sec 5, 7]
*   React Frontend Testing: Using Vitest for unit tests and Playwright for end-to-end tests. [Source: frontend-react/package.json]

### Backend Shared Components (`backend/app/shared/`)

**Purpose:**
The `backend/app/shared/` directory is designated for common, reusable components that are not tightly coupled to any single feature or domain within the backend application. These components provide foundational utilities, definitions, and interfaces used across multiple parts of the system.

**Structure:**
The `shared/` directory is organized into subdirectories based on the type of component:
- `clients/`: External service client instances or client-related code.
- `constants/`: Static constant values and enumerations (Enums).
- `exceptions/`: Custom exception classes used application-wide.
- `schemas/`: Pydantic models representing core internal data structures (distinct from API or DB models).
- `utils/`: General-purpose helper functions.

**Criteria for Inclusion:**
- The component must be genuinely reusable by two or more distinct features or layers of the application.
- It should not contain business logic specific to a single feature.
- It should be relatively stable and not frequently change based on feature requirements.

**Python Package Pattern:**
Each subdirectory within `shared/` is treated as a Python package. Code is typically placed in a module file within the subdirectory (e.g., `exceptions.py` in `exceptions/`). An `__init__.py` file in the subdirectory is used to selectively import and re-export the public items from the module file(s), providing a clean import interface.

**Import Style:**
Components from `shared/` should be imported using the pattern `from app.shared.<subdirectory> import <ItemName>`. Avoid importing directly from module files within the subdirectories (e.py., `from app.shared.exceptions.exceptions import ...`).
