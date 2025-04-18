# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-04-18 09:29:10 - Log of updates made.

*

## Coding Patterns

*   Dependency Injection (via FastAPI). [Source: README.md Sec 6.c]
*   Use SAQ `Status` enum for background task status consistency. [Source: backend/README.md Sec SAQ Limitations]
*   Use SQLAlchemy ORM for database operations within SAQ hooks. [Source: backend/README.md Sec SAQ Limitations]
*   Error Handling: Catch exceptions in SAQ hooks, let SAQ handle task failures (log & re-raise in tasks). [Source: backend/README.md Sec SAQ Limitations]
*   SAQ Usage: Prioritize understanding SAQ patterns, syntax, and implementation by referencing the existing code within the `@/backend/app/worker` directory. For supplementary information, official documentation, or features not demonstrated locally, consult the official SAQ repository: `https://github.com/tobymao/saq/tree/main/saq`.
*   Code Quality: Enforced via pre-commit hooks (Ruff, Black, ESLint, Prettier). [Source: README.md Sec 7]
*   Authentication Overrides: Use SuperTokens API overrides to integrate with our database models, ensuring user data synchronization between SuperTokens and our database. [Source: backend/app/features/auth/supertokens_config.py]
*   React State Management: Use React hooks (useState, useContext, etc.) for state management. [Source: frontend-react/src/contexts/AuthContext.tsx]

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
*   Centralized Base URL Configuration: Using `settings.APP_BASE_URL` from `config.py` for all application URLs (e.g., SuperTokens configuration). [Source: backend/app/features/auth/supertokens_config.py, backend/app/config.py]
*   API Protection: Using SuperTokens session verification as a FastAPI dependency to protect routes. [Source: backend/app/api/routers/agent.py]
*   Required User Dependency: Using `get_required_user_from_session` to ensure a valid user exists for authenticated endpoints. [Source: backend/app/features/auth/supertokens_config.py, backend/app/api/routers/agent.py, backend/app/api/routers/user.py]
*   Docker-Based Development & Deployment: Using Docker Compose for consistent local environments and deployment. [Source: docker-compose.yaml]

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

## Testing Patterns

*   Backend Testing: Unit/integration tests using `pytest`. [Source: backend/README.md Sec Testing]
*   Frontend Testing: Framework/details likely in `frontend/README.md`. [Source: README.md Sec 5, 7]
*   React Frontend Testing: Using Vitest for unit tests and Playwright for end-to-end tests. [Source: frontend-react/package.json]
*   CI Integration: Automated test execution via CI pipelines (e.g., GitHub Actions). [Source: README.md Sec 7]

[2025-04-18 09:29:10] - Added React 19.1, Mantine 7.17.4, and SuperTokens Auth React frontend patterns.
[2025-04-17 12:34:00] - Added authentication patterns for both backend and frontend.
[2025-04-17 09:09:12] - Added SAQ usage guideline and updated patterns based on READMEs.
[2025-04-18 15:23:00] - Updated frontend patterns after code review: Removed manual token handling, custom ProtectedRoute, and clarified auth state source.
