# Backend Service README

This README provides detailed information specifically for the backend service
(FastAPI API and SAQ Worker).

## Overview

*(Briefly describe the purpose of the backend: what APIs it provides, what background tasks it runs)*

## Local Development Setup

*(Provide step-by-step instructions beyond the root README, if necessary)*
*   Prerequisites (e.g., specific Python version, Poetry/PDM installation)
*   Environment Variable Setup (`.env` details specific to backend)
*   Installing Dependencies (`poetry install` or `pdm install`)
*   Running the API server locally (e.g., `uvicorn app.main:app --reload --port 8000`)
*   Running the Worker locally (e.g., `saq app.worker.settings.queue`)

## Database Migrations (Alembic)

*   Generating a new migration script:
    ```bash
    # Example command (run from inside the backend container or with venv active)
    docker-compose exec backend alembic revision --autogenerate -m "Description of changes"
    # OR (if using local venv)
    # alembic revision --autogenerate -m "Description of changes"
    ```
*   Applying migrations:
    ```bash
    docker-compose exec backend alembic upgrade head
    # OR (if using local venv)
    # alembic upgrade head
    ```
*   Downgrading migrations:
    ```bash
    docker-compose exec backend alembic downgrade -1 # (Or specify a specific revision)
    # OR (if using local venv)
    # alembic downgrade -1
    ```

## Running Tests

*   Command to run all tests (e.g., using pytest):
    ```bash
    docker-compose exec backend pytest tests/
    # OR (if using local venv)
    # pytest tests/
    ```
*   Running specific tests.
*   Code coverage instructions.

## Code Style & Linting

*   Tools used (e.g., Ruff, MyPy).
*   Command to run linters/formatters (e.g., `ruff check .`, `ruff format .`).
*   Pre-commit hook information (if used).

## Deployment

*(Brief notes on how the backend is deployed, referencing the root README's deployment strategy)*
*   Dockerfile: `backend/Dockerfile`
*   Entrypoints for API vs Worker (how they are specified in Docker Compose / PaaS).

## Key Components & Structure

*(Optionally, reiterate or add detail to the structure described in the root README, focusing on backend-specific aspects)*
*   `app/main.py`: FastAPI app setup.
*   `app/config.py`: Configuration loading.
*   `app/api/`: API endpoints, schemas, dependencies.
*   `app/worker/`: Background task definitions and settings.
*   `app/db/`: Database models, session, migrations.
*   `app/shared/`: Shared utilities, exceptions, constants.
*   `app/features/`: Business logic modules (e.g., `voice_dna`).
*   `tests/`: Automated tests.
