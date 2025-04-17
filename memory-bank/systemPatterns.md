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
*   Code Quality: Enforced via pre-commit hooks (Ruff, Black, ESLint, Prettier). [Source: README.md Sec 7]

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

## Testing Patterns

*   Backend Testing: Unit/integration tests using `pytest`. [Source: backend/README.md Sec Testing]
*   Frontend Testing: Framework/details likely in `frontend/README.md`. [Source: README.md Sec 5, 7]
*   CI Integration: Automated test execution via CI pipelines (e.g., GitHub Actions). [Source: README.md Sec 7]

[2025-04-17 08:52:21] - Updated patterns based on root and backend READMEs.
