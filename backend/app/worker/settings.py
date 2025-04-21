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

import logging
from datetime import datetime, timezone
from typing import Any, Dict

from sqlalchemy import select
from saq import Queue

from app.config import get_settings  # Import get_settings
from app.db.models import BackgroundJob
from app.db.session import async_session_factory
from app.shared.constants.constants import (
    Status as JobStatus,
)  # Use SAQ's Status enum directly
from app.worker.tasks import poc_test_task

logger = logging.getLogger(__name__)

# Create queue using SAQ's proper connection management
queue = Queue.from_url(get_settings().REDIS_URL, name="default")


async def startup(ctx: Dict[str, Any]) -> None:
    """
    Startup hook for the SAQ worker.

    Runs once when the worker starts before processing any jobs.
    """
    logger.info("SAQ Worker starting up")
    # Store the async session factory in the context
    ctx["db_session_factory"] = async_session_factory


async def shutdown(ctx: Dict[str, Any]) -> None:
    """
    Shutdown hook for the SAQ worker.

    Runs once when the worker is gracefully shutting down.
    """
    logger.info("SAQ Worker shutting down")


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
    # Properly extract function name from the job function
    if hasattr(job, "function"):
        if callable(job.function):
            task_name = job.function.__name__
        else:
            # If it's a string, use it directly
            task_name = str(job.function)
    else:
        task_name = "unknown"

    # Extract metadata for tracking if available
    kwargs = job.kwargs or {}
    user_id = kwargs.get("user_id")
    project_id = kwargs.get("project_id")

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        logger.error("No database session factory found in worker context")
        return

    now = datetime.now(timezone.utc)

    try:
        async with session_factory() as session:
            async with session.begin():
                # Check if job record exists using proper SQLAlchemy query
                stmt = select(BackgroundJob).where(BackgroundJob.job_id == job_id)
                result = await session.execute(stmt)
                job_record = result.scalar_one_or_none()

                if job_record:
                    # Update existing record using ORM
                    job_record.status = JobStatus.ACTIVE.value
                    job_record.started_at = now
                    job_record.task_name = task_name
                    if user_id:
                        job_record.user_id = user_id
                    if project_id:
                        job_record.project_id = project_id
                else:
                    # Create new record using SQLAlchemy ORM
                    new_record = BackgroundJob(
                        job_id=job_id,
                        task_name=task_name,
                        status=JobStatus.ACTIVE.value,
                        started_at=now,
                        created_at=now,
                        user_id=user_id,
                        project_id=project_id,
                    )
                    session.add(new_record)

        logger.info(
            f"Job tracking record created/updated - job_id: {job_id}, task: {task_name}, status: {JobStatus.ACTIVE.value}"
        )

    except Exception as e:
        # Log the error but don't prevent the task from running
        logger.exception(f"Error in before_process hook for job {job_id}: {str(e)}")


async def after_process(ctx: Dict[str, Any]) -> None:
    """
    After-process hook that runs after each job execution.

    Updates the job record in the background_jobs table with final status,
    result data or error message, and completion timestamp.
    """
    job = ctx.get("job")
    if not job:
        logger.warning("No job found in context for after_process hook")
        return

    job_id = job.id
    job_status = job.status  # This is the SAQ Status enum value

    result = ctx.get("result")
    error = ctx.get("error")

    session_factory = ctx.get("db_session_factory")
    if not session_factory:
        logger.error("No database session factory found in worker context")
        return

    now = datetime.now(timezone.utc)

    try:
        async with session_factory() as session:
            async with session.begin():
                # Use SQLAlchemy query to get the job record
                stmt = select(BackgroundJob).where(BackgroundJob.job_id == job_id)
                result_query = await session.execute(stmt)
                job_record = result_query.scalar_one_or_none()

                if job_record:
                    # Update the job record using ORM
                    job_record.status = job_status.value
                    job_record.completed_at = now

                    if job_status == JobStatus.FAILED:
                        job_record.error_message = (
                            str(error) if error else "Unknown error"
                        )
                        job_record.result = None  # Clear any previous result
                    elif job_status == JobStatus.COMPLETE:
                        job_record.result = result
                        job_record.error_message = None  # Clear any previous error

                    logger.info(
                        f"Job tracking record updated - job_id: {job_id}, status: {job_status.value}"
                    )
                else:
                    logger.warning(f"No job record found for job_id: {job_id}")

    except Exception as e:
        # Log the error (the task has already completed or failed at this point)
        logger.exception(f"Error in after_process hook for job {job_id}: {str(e)}")


# SAQ Settings using only supported hooks in v0.22.5
settings = {
    "queue": queue,
    "concurrency": 5,
    "functions": [poc_test_task],
    "startup": startup,
    "shutdown": shutdown,
    "before_process": before_process,
    "after_process": after_process,
}
