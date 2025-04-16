# Backend Service README

This README provides detailed information specifically for the backend service
(FastAPI API and SAQ Worker).

## Overview

The backend service provides the core functionality for the AI Video Creation Platform, consisting of:

- **FastAPI API Server**: Handles HTTP requests for user interactions, project management, and AI processing
- **SAQ Worker**: Processes background tasks like AI analysis, embeddings generation, and long-running operations
- **PostgreSQL Database**: Stores all user data, project information, and AI-generated content with pgvector extension for vector search capabilities

## Local Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 17 with pgvector extension

### Environment Setup
1. Copy `.env.example` to `.env` in the `backend/` directory
2. Update the DATABASE_URL and other environment variables as needed

### Running with Docker (Recommended)
The easiest way to run the backend is using Docker Compose from the project root:
```bash
docker-compose up -d
```

This starts the API server, worker, PostgreSQL database, and Redis server.

### Running Locally (Development)
For local development without Docker:
```bash
# Install dependencies
pip install -e .

# Run the API server
uvicorn app.main:app --reload --port 8000

# Run the worker (in a separate terminal)
python -m app.worker.run
```

## Database Migrations (Alembic)

The project uses Alembic for database migrations. Migrations are stored in `app/db/migrations/`.

### Initial Setup
The database is configured with all necessary tables and the pgvector extension for vector embeddings. When starting a fresh instance:

```bash
# Apply all migrations
docker-compose exec backend alembic upgrade head
```

### Working with Migrations

1. **Generate a new migration after model changes:**
    ```bash
    # Run from inside the backend container
    docker-compose exec backend alembic revision --autogenerate -m "Description of changes"
    ```

2. **Apply pending migrations:**
    ```bash
    docker-compose exec backend alembic upgrade head
    ```

3. **View migration history:**
    ```bash
    docker-compose exec backend alembic history
    ```

4. **Downgrade to a previous version:**
    ```bash
    # Downgrade one step
    docker-compose exec backend alembic downgrade -1

    # Downgrade to a specific revision
    docker-compose exec backend alembic downgrade revision_id
    ```

5. **Get current migration version:**
    ```bash
    docker-compose exec backend alembic current
    ```

### Migration Configuration
- **alembic.ini**: Located at `backend/alembic.ini` - contains basic Alembic configuration
- **env.py**: Located at `app/db/migrations/env.py` - configures how Alembic connects to the database and loads models
- **Database URL**: Loaded from environment variables via `app.config.settings`
- **Models**: Loaded from `app.db.models` which defines the SQLAlchemy models

### Vector Search Support
The database is configured with pgvector extension for embedding storage and similarity search. The `retrievable_text` table includes a VECTOR(1536) column with an IVFFLAT index for efficient similarity searches.

## Running Tests

### Running Tests
```bash
# Run all tests
docker-compose exec backend pytest

# Run tests with coverage report
docker-compose exec backend pytest --cov=app tests/

# Run specific test file
docker-compose exec backend pytest tests/test_specific_module.py

# Run tests matching a specific name pattern
docker-compose exec backend pytest -k "test_pattern"
```

## Code Style & Linting

The project uses:
- **Ruff**: For linting and code formatting
- **MyPy**: For static type checking

```bash
# Run linting
docker-compose exec backend ruff check .

# Run formatting
docker-compose exec backend ruff format .

# Run type checking
docker-compose exec backend mypy app/
```

Pre-commit hooks are configured in `.pre-commit-config.yaml` in the project root to automatically run these checks before commits.

### Type Checking Configuration

The project uses SQLAlchemy 2.0 which includes built-in type annotations. MyPy is configured to work with these annotations through:

- **`.mypy.ini`**: Located at `backend/.mypy.ini` - contains settings for the SQLAlchemy plugin
- **SQLAlchemy Plugin**: The configuration includes the SQLAlchemy plugin (`sqlalchemy.ext.mypy.plugin`) which enables proper type checking of SQLAlchemy ORM models
- **Pre-commit Integration**: The mypy pre-commit hook is configured to use the system Python (your virtual environment) and the project's mypy configuration

For SQLAlchemy 2.0 type checking to work correctly:
- Do not install `sqlalchemy-stubs` as it conflicts with SQLAlchemy 2.0's built-in typing
- Ensure `sqlalchemy[mypy]` is installed in your development environment

## Deployment

The backend is deployed as a containerized application. See the root README.md for complete deployment details.

- **Dockerfile**: `backend/Dockerfile` - a multi-stage build that creates a single image used for both API and worker services
- **API Entrypoint**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Worker Entrypoint**: `python -m app.worker.run`

Both services use the same Docker image but different commands, allowing for better resource utilization and simplified deployment.

## Key Components & Structure

The backend follows a modular architecture:

- **`app/main.py`**: FastAPI application initialization, middleware setup, and API router inclusion
- **`app/config.py`**: Environment configuration using Pydantic settings
- **`app/api/`**: API endpoints, request/response schemas, and dependencies
  - **`routers/`**: Endpoint grouping by feature
  - **`dependencies.py`**: Common API dependencies (auth, DB session, etc.)
  - **`schemas.py`**: Pydantic models for API request/response validation
- **`app/worker/`**: Background job processing using SAQ
  - **`settings.py`**: Queue configuration
  - **`run.py`**: Worker entrypoint
- **`app/db/`**: Database layer
  - **`models.py`**: SQLAlchemy ORM models (with metadata for Alembic)
  - **`session.py`**: Database connection handling
  - **`migrations/`**: Alembic migration scripts
- **`app/shared/`**: Cross-cutting concerns
  - **`clients/`**: External API clients
  - **`utils.py`**: Common utilities
  - **`exceptions.py`**: Custom exception classes
- **`app/features/`**: Business logic modules organized by domain
  - Each feature has consistent structure (service.py, tasks.py, pipelines.py)
- **`tests/`**: Automated tests mirroring the application structure

## Database Schema

The database schema is defined in SQLAlchemy models in `app/db/models.py` and includes:

- **Users & Authentication**: User accounts and authentication data
- **Projects & Content**: Project structure, content sources, and generated scripts
- **AI Analysis**: DNA profiles, research analysis, and safety checks
- **Vector Storage**: Retrievable text chunks with vector embeddings for semantic search
- **Background Processing**: Job tracking and task management

See `database_design.md` for complete schema details and entity relationships.
