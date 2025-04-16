# Backend Service

## Overview

This directory contains the backend API and worker components of the AI Video Creation Platform. The backend is built with FastAPI and employs SAQ (Simple Async Queue) for background task processing. It uses SQLAlchemy for database operations and PostgreSQL as the database.

## Setup & Running Locally

1. Install dependencies:
   ```bash
   cd backend
   pip install -e .
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your local settings
   ```

3. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

4. Run the API server locally (development mode):
   ```bash
   uvicorn app.main:app --reload
   ```

5. Run the worker locally:
   ```bash
   saq app.worker.settings.settings
   ```

## Docker-based Development

When using the Docker setup defined in the root directory:

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Apply migrations:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

3. View logs:
   ```bash
   docker-compose logs -f backend  # API server logs
   docker-compose logs -f worker   # Background worker logs
   ```

## Background Task Architecture

### SAQ Implementation

The project uses SAQ (Simple Async Queue) for asynchronous background task processing. The implementation follows these key patterns:

1. **Queue Configuration**:
   - Redis-backed queue defined in `app/worker/settings.py`
   - Named "default" queue for standard tasks
   - Uses the application's `REDIS_URL` configuration

2. **Lifecycle Hooks**:
   - `startup`: Initializes database session factory in worker context
   - `shutdown`: Performs cleanup when worker process terminates
   - `before_process`: Records task start in database with `Status.ACTIVE`
   - `after_process`: Updates task status to `Status.COMPLETE` or `Status.FAILED` with results/errors

3. **Task Status Tracking**:
   - Uses native SAQ `Status` enum values: `NEW`, `QUEUED`, `ACTIVE`, `COMPLETE`, `FAILED`, etc.
   - Status values stored directly in `background_jobs` table

4. **Database Integration**:
   - Tasks tracked in `background_jobs` table
   - Uses SQLAlchemy ORM for database operations
   - Records job_id, task_name, status, user/project context, results, errors

### API/Worker Flow

1. Client calls API endpoint (e.g., `/api/v1/tasks/trigger-test`)
2. API enqueues a task via SAQ's `queue.enqueue()` method
3. API returns the job ID to the client with 202 Accepted status
4. Worker's `before_process` hook creates/updates a database record with `Status.ACTIVE`
5. Worker executes the task function
6. Worker's `after_process` hook updates the database record with final status and results
7. Client can query task status via API endpoint using the job ID

### SAQ Task Implementation Guide

To implement a new background task:

1. Define the task function in an appropriate module under `app/worker/tasks.py` or feature-specific files:

```python
async def my_example_task(
    ctx: Context,
    *,
    param1: str,
    param2: Optional[int] = None,
    user_id: Optional[uuid.UUID] = None,
    project_id: Optional[uuid.UUID] = None,
) -> Dict[str, Any]:
    """
    Example task processing.

    Args:
        ctx: SAQ context containing job information
        param1: Example required parameter
        param2: Example optional parameter
        user_id: User who initiated the task (optional)
        project_id: Related project (optional)

    Returns:
        Result dictionary that will be stored in the database
    """
    # Get job ID for logging
    job = ctx.get("job")
    job_id = job.id if job else "unknown"

    try:
        # Task implementation here
        # ...

        # Return result as a serializable dictionary
        return {
            "status": "success",
            "result_data": "your result here",
        }
    except Exception as e:
        # Log the error and re-raise to allow SAQ to handle failure
        logger.exception(f"Error in my_example_task: {str(e)}")
        raise
```

2. Register the task in `app/worker/settings.py`:

```python
# Add import
from app.worker.tasks import my_example_task

# Add to functions list in settings
settings = {
    "queue": queue,
    "concurrency": 5,
    "functions": [
        poc_test_task,
        my_example_task,  # Add your new task here
    ],
    "startup": startup,
    "shutdown": shutdown,
    "before_process": before_process,
    "after_process": after_process,
}
```

3. Create an API endpoint to trigger the task:

```python
@router.post("/tasks/my-example", status_code=status.HTTP_202_ACCEPTED)
async def trigger_example_task(payload: YourRequestModel) -> YourResponseModel:
    try:
        # Convert to task parameters
        task_kwargs = payload.dict(exclude_unset=True)

        # Enqueue the task
        job = await queue.enqueue("my_example_task", **task_kwargs)

        return YourResponseModel(
            message="Task accepted",
            job_id=job.id,
        )
    except Exception as e:
        logger.exception(f"Failed to enqueue task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enqueue task",
        )
```

### Known Limitations and Workarounds

1. **SAQ Version 0.22.5+ Hook Limitations**:
   - SAQ 0.22.5+ supports only `startup`, `shutdown`, `before_process`, and `after_process` hooks
   - Additional hooks like `before_complete`, `before_retry`, and `on_success` are planned for future SAQ versions
   - Current workaround: Implement all logic in `before_process` and `after_process` hooks

2. **Status Representation**:
   - Always use the SAQ `Status` enum (imported from `saq.job`) for consistency
   - Avoid hardcoded status strings

3. **Database Integration**:
   - Always use SQLAlchemy ORM for database operations in hooks
   - Avoid raw SQL strings due to injection risks and lack of type safety
   - Properly manage sessions with `async with` contexts

4. **Error Handling**:
   - Catch exceptions in hooks but not in tasks (let SAQ handle task failures)
   - Log exceptions before re-raising in tasks
   - Use log levels appropriately (DEBUG, INFO, WARNING, ERROR)

## Database Migrations

Generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

## Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
