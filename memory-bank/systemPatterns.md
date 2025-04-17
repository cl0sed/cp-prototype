# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-04-17 08:43:50 - Log of updates made.

*

## Coding Patterns

*   Dependency Injection (via FastAPI). [Source: README.md Sec 6.c]
*   Use SAQ `Status` enum for background task status consistency. [Source: backend/README.md Sec SAQ Limitations]
*   Use SQLAlchemy ORM for database operations within SAQ hooks. [Source: backend/README.md Sec SAQ Limitations]
*   Error Handling: Catch exceptions in SAQ hooks, let SAQ handle task failures (log & re-raise in tasks). [Source: backend/README.md Sec SAQ Limitations]
*   SAQ Usage: Prioritize understanding SAQ patterns, syntax, and implementation by referencing the existing code within the `@/backend/app/worker` directory. For supplementary information, official documentation, or features not demonstrated locally, consult the official SAQ repository: `https://github.com/tobymao/saq/tree/main/saq`.
*   Code Quality: Enforced via pre-commit hooks (Ruff, Black, ESLint, Prettier). [Source: README.md Sec 7]
*   Authentication Overrides: Use SuperTokens API overrides to integrate with our database models, ensuring user data synchronization between SuperTokens and our database. [Source: backend/app/features/auth/supertokens_config.py]

## Architectural Patterns

*   Monorepo Structure: Centralized management of frontend, backend, and configs. [Source: README.md Sec 5]
*   Async-first Design: Leveraging async capabilities in FastAPI and SAQ. [Source: README.md Sec 6.b, 6.c]
*   Single Backend Docker Image: Bundles API and Worker for simplified deployment. [Source: README.md Sec 6.c]
*   API/Worker Split: API for synchronous requests & task triggering, Worker for asynchronous/long-running tasks. [Source: README.md Sec 6.d, backend/README.md Sec SAQ]
*   Background Task Queue: Using SAQ library with Redis as the broker. [Source: README.md Sec 6.a, backend/README.md Sec SAQ]
*   LLM Gateway Abstraction: Using Portkey to manage interactions with external LLMs. [Source: README.md Sec 6.a, 6.f]
*   Vector Database for RAG: Utilizing PostgreSQL with the `pgvector` extension. [Source: README.md Sec 6.a, 6.e]
*   Database Migrations: Managed via Alembic. [Source: README.md Sec 6.a, 7]
*   Deployment Target: Container-based PaaS. [Source: README.md Sec 6.a]
*   Configuration Management: Primarily via environment variables (local via `.env`, deployed via platform secrets). [Source: README.md Sec 7]
*   Authentication Architecture: Using SuperTokens Managed Service with a two-tier approach - SuperTokens for auth management and our database for user data, linked via `supertokens_user_id`. [Source: backend/app/features/auth/supertokens_config.py]
*   API Protection: Using SuperTokens session verification as a FastAPI dependency to protect routes. [Source: backend/app/api/routers/agent.py]

## Frontend Patterns

*   Authentication UI: Using SuperTokens pre-built UI components via catch-all routes for authentication flows. [Source: frontend/src/routes/auth/[[...path]]/+page.svelte]
*   API Client: Wrapping fetch calls with SuperTokens Session.fetch to automatically handle authentication tokens. [Source: frontend/src/lib/services/apiClient.ts]
*   Authentication State: Checking authentication status on component mount and updating UI accordingly. [Source: frontend/src/routes/+layout.svelte]
*   Protected Routes: Client-side route protection by checking authentication status and redirecting if not authenticated. [Source: frontend/src/routes/dashboard/+page.svelte]

## Testing Patterns

*   Backend Testing: Unit/integration tests using `pytest`. [Source: backend/README.md Sec Testing]
*   Frontend Testing: Framework/details likely in `frontend/README.md`. [Source: README.md Sec 5, 7]
*   CI Integration: Automated test execution via CI pipelines (e.g., GitHub Actions). [Source: README.md Sec 7]

[2025-04-17 09:09:12] - Added SAQ usage guideline and updated patterns based on READMEs.
[2025-04-17 12:34:00] - Added authentication patterns for both backend and frontend.
