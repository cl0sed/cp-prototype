"""
SAQ Worker Settings.

This module configures the SAQ queue and worker settings, including:
- Queue instantiation
- Task registration
- Lifecycle hooks (startup, shutdown, before_process, after_process)
- Concurrency settings

The worker context (ctx) is used to share state and utilities across
lifecycle hooks and task functions.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy import text
from saq import Queue
# Import types from the correct location

from app.config import settings
from app.db.session import async_session_factory
from app.worker.tasks import poc_test_task

# Configure module-level logger with more verbose output for debugging
logger = logging.getLogger(__name__)

# Define a type for the SAQ settings dictionary
SaqSettings = Dict[str, Any]

# Create the SAQ queue from Redis URL in app settings
queue = Queue.from_url(settings.REDIS_URL, name="default")


async def startup(ctx: Dict[str, Any]) -> None:
    """
    Startup hook for the SAQ worker.

    This runs once when the worker starts, before processing any jobs.
    It initializes resources needed by all tasks, such as database connections.

    Args:
        ctx: The worker context dict where we store shared resources
    """
    logger.info("SAQ Worker starting up")

    # Store the async session factory in the context
    # This allows tasks to create their own database sessions as needed
    ctx["db_session_factory"] = async_session_factory


async def shutdown(ctx: Dict[str, Any]) -> None:
    """
    Shutdown hook for the SAQ worker.

    This runs once when the worker is gracefully shutting down.
    Use this to clean up any resources initialized in startup.

    Args:
        ctx: The worker context dict
    """
    logger.info("SAQ Worker shutting down")
    # The async_session_factory doesn't need explicit cleanup


async def before_process(ctx: Dict[str, Any]) -> None:
    """
    Before-process hook that runs before each job execution.

    This hook creates or updates the job record in the background_jobs table
    with status='active' and the current timestamp.

    Args:
        ctx: The worker context dict containing job info and shared resources
    """
    # Extract the job object from the context
    job = ctx.get("job")
    if not job:
        logger.warning("No job found in context for before_process hook")
        return

    # Get job details
    job_id = job.id

    # In SAQ, the function attribute is either a function object or a string with the task name
    if hasattr(job, "function"):
        if callable(job.function):
            task_name = job.function.__name__
        else:
            # If it's a string, use it directly
            task_name = str(job.function)
    else:
        task_name = "unknown"

    # Get database session factory
    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        logger.error("No database session factory found in worker context")
        return

    # Current timestamp for started_at
    now = datetime.now(timezone.utc)

    try:
        # Create database session
        async with session_factory() as session:
            # Log the task details
            logger.info(f"Processing task {task_name} with job_id {job_id}")

            async with session.begin():
                # Upsert job record (INSERT ... ON CONFLICT DO UPDATE)
                # Using direct SQL to avoid potential ORM-related issues
                query = f"""
                INSERT INTO background_jobs (job_id, task_name, status, started_at, created_at)
                VALUES ('{job_id}', '{task_name}', 'active', '{now.isoformat()}', '{now.isoformat()}')
                ON CONFLICT (job_id) DO UPDATE
                SET status = 'active',
                    started_at = '{now.isoformat()}',
                    task_name = '{task_name}'
                """

                await session.execute(text(query))

        logger.info(
            f"Job tracking record created/updated - job_id: {job_id}, task: {task_name}, status: active"
        )

    except Exception as e:
        # Log the error but don't prevent the task from running
        logger.exception(f"Error in before_process hook for job {job_id}: {str(e)}")


async def after_process(ctx: Dict[str, Any]) -> None:
    """
    After-process hook that runs after each job execution.

    This hook updates the job record in the background_jobs table with final status,
    result data or error message, and completion timestamp.

    Args:
        ctx: The worker context dict containing job info, result/error, and shared resources
    """
    # Extract the job object from the context
    job = ctx.get("job")
    if not job:
        logger.warning("No job found in context for after_process hook")
        return

    # Get job details
    job_id = job.id
    job_status = str(job.status)  # Convert to string to handle enum-like values

    # DEEP DEBUGGING: Print all context keys
    logger.info(f"CONTEXT KEYS: {list(ctx.keys())}")

    # Get result if available
    result = ctx.get("result")
    logger.info(f"Result in context: {result}")

    # Save result from job directly if context doesn't have it
    if result is None and hasattr(job, "result"):
        result = job.result
        logger.info(f"Result from job: {result}")

    # Get error if any
    error = ctx.get("error")

    # Get database session factory
    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        logger.error("No database session factory found in worker context")
        return

    # Current timestamp for completed_at
    now = datetime.now(timezone.utc)

    try:
        # Directly use a raw SQL string for maximum control
        if job_status.upper() == "STATUS.COMPLETE" or "COMPLETE" in job_status.upper():
            # For completed jobs
            logger.info(f"Job completed successfully: {job_id}")

            if result:
                # Convert result to JSON string
                try:
                    result_json = json.dumps(result)
                    logger.info(f"Serialized result to JSON: {result_json[:200]}")

                    # Use direct SQL with the JSONB type explicitly cast
                    query = f"""
                    UPDATE background_jobs
                    SET
                        status = '{job_status}',
                        completed_at = '{now.isoformat()}',
                        result = '{result_json.replace("'", "''")}'::jsonb
                    WHERE job_id = '{job_id}'
                    """
                    logger.info(f"Executing SQL with result: {query[:200]}...")

                    async with session_factory() as session:
                        async with session.begin():
                            await session.execute(text(query))
                            logger.info(f"Updated job {job_id} with result")
                except Exception as e:
                    logger.exception(f"Error serializing or storing result: {e}")
                    # Fallback to basic update without result
                    async with session_factory() as session:
                        async with session.begin():
                            query = f"""
                            UPDATE background_jobs
                            SET status = '{job_status}',
                                completed_at = '{now.isoformat()}'
                            WHERE job_id = '{job_id}'
                            """
                            await session.execute(text(query))
                            logger.info(
                                f"Updated job {job_id} with basic info (result failed)"
                            )
            else:
                # No result available
                logger.warning(f"No result found for completed job {job_id}")
                async with session_factory() as session:
                    async with session.begin():
                        query = f"""
                        UPDATE background_jobs
                        SET status = '{job_status}',
                            completed_at = '{now.isoformat()}'
                        WHERE job_id = '{job_id}'
                        """
                        await session.execute(text(query))
        elif job_status.upper() == "STATUS.FAILED" or "FAILED" in job_status.upper():
            # For failed jobs
            logger.info(f"Job failed: {job_id}, error: {error}")
            async with session_factory() as session:
                async with session.begin():
                    error_str = (
                        str(error).replace("'", "''") if error else "Unknown error"
                    )
                    query = f"""
                    UPDATE background_jobs
                    SET
                        status = '{job_status}',
                        completed_at = '{now.isoformat()}',
                        error_message = '{error_str}'
                    WHERE job_id = '{job_id}'
                    """
                    await session.execute(text(query))
        else:
            # For other statuses
            logger.info(f"Job has status {job_status}: {job_id}")
            async with session_factory() as session:
                async with session.begin():
                    query = f"""
                    UPDATE background_jobs
                    SET status = '{job_status}',
                        completed_at = '{now.isoformat()}'
                    WHERE job_id = '{job_id}'
                    """
                    await session.execute(text(query))

        logger.info(
            f"Job tracking record updated - job_id: {job_id}, status: {job_status}"
        )

    except Exception as e:
        # Log the error (the task has already completed or failed at this point)
        logger.exception(f"Error in after_process hook for job {job_id}: {str(e)}")


# SAQ requires a dictionary called 'settings' based on its import conventions
# Export it as a module attribute for the SAQ CLI to find
# NOTE: we're using a workaround with # type: ignore to bypass the mypy name conflict error
# The import is still available for use inside this module, but we need the name 'settings'
# at module level for SAQ to work correctly.
settings: SaqSettings = {  # type: ignore
    "queue": queue,
    "concurrency": 5,
    "functions": [
        poc_test_task,
    ],
    "startup": startup,
    "shutdown": shutdown,
    "before_process": before_process,
    "after_process": after_process,
}
