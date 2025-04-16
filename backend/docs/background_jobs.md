# Background Job Processing with SAQ

## Overview

The AI Video Creation Platform uses SAQ (Simple Async Queue) to handle asynchronous background processing tasks. This document provides detailed information on how the background job system is implemented, including configuration, database integration, and best practices for creating new tasks.

## Architecture

### Core Components

1. **SAQ Queue**: A Redis-backed asynchronous job queue configured in `app/worker/settings.py`
2. **Worker Process**: Runs separately from the API server, processes jobs from the queue
3. **Database Integration**: Tracks job status and results in the `background_jobs` table
4. **API Endpoints**: Trigger tasks and allow clients to query job status

### Job Lifecycle

1. **Job Creation**: API endpoint enqueues a task with `queue.enqueue()`
2. **Queuing**: Task is stored in Redis, ready for processing
3. **Processing Start**: Worker picks up task, runs `before_process` hook to update DB
4. **Execution**: Worker executes the task function
5. **Completion/Failure**: Worker runs `after_process` hook to update DB with result/error
6. **Result Retrieval**: Client queries API to get job status and results

## Implementation Details

### Configuration in `app/worker/settings.py`

The SAQ worker is configured with a settings dictionary that includes:

```python
settings = {
    "queue": queue,              # Redis queue instance
    "concurrency": 5,            # Number of concurrent tasks
    "functions": [               # List of task functions
        poc_test_task,
        # Add other tasks here
    ],
    "startup": startup,          # Run when worker starts
    "shutdown": shutdown,        # Run when worker stops
    "before_process": before_process,  # Run before each task
    "after_process": after_process,    # Run after each task
}
```

### Database Integration

Tasks are tracked in the `background_jobs` table, which has the following structure:

```python
class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    job_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    task_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    project_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id: Mapped[Optional[PyUUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False, index=True)
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True, index=True)
```

### Hooks

#### Startup Hook

```python
async def startup(ctx: Dict[str, Any]) -> None:
    """
    Startup hook for the SAQ worker.

    Runs once when the worker starts before processing any jobs.
    """
    logger.info("SAQ Worker starting up")
    # Store the async session factory in the context
    ctx["db_session_factory"] = async_session_factory
```

#### Before Process Hook

```python
async def before_process(ctx: Dict[str, Any]) -> None:
    """
    Before-process hook that runs before each job execution.

    Creates or updates the job record in the background_jobs table
    with status='active' and the current timestamp.
    """
    job = ctx.get("job")
    if not job:
        logger.warning("No job found in context for before_process hook")
        return

    job_id = job.id
    # Extract task name, user_id, project_id from context

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        logger.error("No database session factory found in worker context")
        return

    now = datetime.now(timezone.utc)

    try:
        async with session_factory() as session:
            async with session.begin():
                # Check if job record exists using SQLAlchemy
                stmt = select(BackgroundJob).where(BackgroundJob.job_id == job_id)
                result = await session.execute(stmt)
                job_record = result.scalar_one_or_none()

                if job_record:
                    # Update existing record with ORM
                    job_record.status = Status.ACTIVE.value
                    job_record.started_at = now
                    # Update other fields
                else:
                    # Create new record with SQLAlchemy ORM
                    new_record = BackgroundJob(
                        job_id=job_id,
                        task_name=task_name,
                        status=Status.ACTIVE.value,
                        started_at=now,
                        created_at=now,
                        # Other fields
                    )
                    session.add(new_record)
    except Exception as e:
        logger.exception(f"Error in before_process hook: {str(e)}")
```

#### After Process Hook

```python
async def after_process(ctx: Dict[str, Any]) -> None:
    """
    After-process hook that runs after each job execution.

    Updates the job record with final status, result data or error message,
    and completion timestamp.
    """
    job = ctx.get("job")
    if not job:
        logger.warning("No job found in context for after_process hook")
        return

    job_id = job.id
    job_status = job.status  # SAQ Status enum value
    result = ctx.get("result")
    error = ctx.get("error")

    # Get session factory from context

    try:
        async with session_factory() as session:
            async with session.begin():
                # Get the job record with SQLAlchemy
                stmt = select(BackgroundJob).where(BackgroundJob.job_id == job_id)
                result_query = await session.execute(stmt)
                job_record = result_query.scalar_one_or_none()

                if job_record:
                    # Update with ORM
                    job_record.status = job_status.value
                    job_record.completed_at = now

                    if job_status == Status.FAILED:
                        job_record.error_message = str(error) if error else "Unknown error"
                        job_record.result = None  # Clear any previous result
                    elif job_status == Status.COMPLETE:
                        job_record.result = result
                        job_record.error_message = None  # Clear any previous error
    except Exception as e:
        logger.exception(f"Error in after_process hook: {str(e)}")
```

## Task Implementation

Tasks are implemented as asynchronous functions that receive a context object and task-specific parameters. Here's the structure of a typical task:

```python
async def poc_test_task(
    ctx: Context,
    *,
    message: str = "Default message",
    user_id: Optional[uuid.UUID] = None,
    project_id: Optional[uuid.UUID] = None,
) -> Dict[str, Any]:
    """
    A simple test task demonstrating the SAQ worker setup.
    """
    # Get job ID from context
    job = ctx.get("job")
    job_id = job.id if job else "unknown"

    logger.info(f"Starting task - job_id: {job_id}")

    try:
        # Task implementation
        # ...

        # Return result
        return {
            "status": "success",
            "job_id": job_id,
            "processed_message": f"Processed: {message}",
            "metadata": {
                "user_id": str(user_id) if user_id else None,
                "project_id": str(project_id) if project_id else None,
            }
        }
    except Exception as e:
        logger.exception(f"Error in task: {str(e)}")
        # Re-raise to let SAQ handle failure
        raise
```

## API Integration

Tasks are triggered through API endpoints that enqueue the task and return the job ID:

```python
@router.post(
    "/tasks/trigger-test",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TriggerResponse,
)
async def trigger_test_task(payload: TriggerRequest) -> TriggerResponse:
    """
    Trigger a test background task.
    """
    # Prepare task parameters
    task_kwargs = {}
    for k, v in payload.dict().items():
        if v is not None:
            if isinstance(v, uuid.UUID):
                task_kwargs[k] = str(v)
            else:
                task_kwargs[k] = v

    try:
        # Enqueue the task
        job = await queue.enqueue("poc_test_task", **task_kwargs)

        return TriggerResponse(
            message="Task accepted and queued for processing",
            job_id=job.id,
            status=Status.QUEUED.value,
        )
    except Exception as e:
        # Handle errors
        logger.exception(f"Failed to enqueue task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue task: {str(e)}",
        )
```

## Best Practices

### Status Handling

Always use SAQ's native Status enum to ensure consistency:

```python
from saq.job import Status

# In hooks:
job_record.status = Status.ACTIVE.value
job_record.status = Status.COMPLETE.value
job_record.status = Status.FAILED.value
```

### Database Operations

1. Always use SQLAlchemy ORM for database operations:
   - Use `select()` for queries
   - Use direct attribute access for updates
   - Add new records with `session.add()`

2. Properly manage sessions with context managers:
   ```python
   async with session_factory() as session:
       async with session.begin():
           # DB operations
   ```

### Error Handling

1. Catch and log exceptions in hooks to prevent worker crashes
2. Re-raise exceptions in tasks to let SAQ handle the failure flow
3. Use appropriate log levels:
   - DEBUG for detailed diagnostics
   - INFO for general progress
   - WARNING for potential issues
   - ERROR for failures that need attention

## Docker Setup

The worker service is defined in `docker-compose.yaml`:

```yaml
worker:
  build:
    context: ./backend
  container_name: saq_worker
  env_file:
    - ./backend/.env
  volumes:
    - ./backend/app:/app/app
  depends_on:
    db:
      condition: service_healthy
    redis:
      condition: service_healthy
  networks:
    - app_network
  command: saq app.worker.settings.settings
  restart: unless-stopped
```

## Known Limitations and Workarounds

1. **Limited Hook Support in SAQ 0.22.5+**:
   - The current SAQ version (0.22.5+) supports only a subset of hooks: `startup`, `shutdown`, `before_process`, and `after_process`
   - Additional hooks like `before_complete`, `before_retry`, and `on_success` may be supported in future versions
   - Workaround: Implement all necessary tracking logic in the supported hooks

2. **Workflow Orchestration**:
   - Simple SAQ tasks are not designed for complex multi-step workflows
   - Complex orchestration is deferred to a future implementation (post-MVP)

3. **SQLAlchemy Model Errors**:
   - SQLAlchemy initialization errors may occur if model relationships are improperly defined
   - Ensure all foreign keys and relationships are properly configured
   - Fix model errors before adding new tasks

4. **Result Serialization**:
   - Task results must be JSON-serializable
   - Use basic Python types (dict, list, str, int, bool, None) for results
   - Convert UUID objects to strings before returning them

## Troubleshooting

### Worker Fails to Start

If the worker fails to start with errors like:

```
Worker.__init__() got an unexpected keyword argument 'before_complete'
```

Ensure that only supported hooks are included in the `settings` dictionary:
- Supported: `startup`, `shutdown`, `before_process`, `after_process`
- Unsupported: `before_complete`, `before_retry`, `on_success` (in SAQ 0.22.5+)

### Database Errors

For SQLAlchemy errors:

1. Check model definitions for relationship errors
2. Ensure database tables exist and match model definitions
3. Run Alembic migrations to update database schema

### Task Failures

If tasks are failing:

1. Check worker logs for exceptions
2. Verify task parameters and types
3. Ensure context is correctly used in task functions
4. Verify Redis connection
5. Check that the database is properly configured and accessible
