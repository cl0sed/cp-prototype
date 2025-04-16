"""
SAQ Task Definitions.

This module contains the definitions of background tasks to be processed by the SAQ worker.
Each task should be an async function that accepts a Context object as its first parameter,
followed by any task-specific parameters.

Tasks should:
- Be idempotent where possible
- Include appropriate error handling
- Return results that can be serialized to JSON
- Log key events for observability
"""

import asyncio
import logging
import uuid
from typing import Dict, Optional, Any

from saq.types import Context

# Configure module-level logger
logger = logging.getLogger(__name__)


async def poc_test_task(
    ctx: Context,
    *,
    message: str = "Default message",
    user_id: Optional[uuid.UUID] = None,
    project_id: Optional[uuid.UUID] = None,
) -> Dict[str, Any]:
    """
    A simple test task to validate the SAQ worker setup.

    This task simulates a long-running operation with asyncio.sleep
    and returns a basic result dictionary.

    Args:
        ctx: The SAQ context object, containing job information and shared resources
        message: An optional test message to process
        user_id: Optional user ID associated with this task
        project_id: Optional project ID associated with this task

    Returns:
        A dictionary with the job ID, processed message, and status
    """
    # Extract job ID from context for logging and tracking
    job = ctx.get("job")
    job_id = job.id if job else "unknown"

    logger.info(f"Starting poc_test_task - job_id: {job_id}, message: {message}")
    print(f"Starting poc_test_task - job_id: {job_id}, message: {message}")

    try:
        # Simulate work with a delay
        # This represents the "long-running" part of a real background task
        logger.info(f"Processing job {job_id} - simulating work...")
        print(f"Processing job {job_id} - simulating work...")
        await asyncio.sleep(2)

        # Process the message (in this simple case, just add a prefix)
        processed_message = f"Processed: {message}"

        # Create a result that will be stored in the background_jobs table
        result = {
            "status": "success",
            "job_id": job_id,
            "processed_message": processed_message,
            # Include metadata about what user/project this was processed for
            "metadata": {
                "user_id": str(user_id) if user_id else None,
                "project_id": str(project_id) if project_id else None,
            },
        }

        logger.info(f"Completed poc_test_task - job_id: {job_id}")
        print(f"Completed poc_test_task - job_id: {job_id}")
        print(f"Result: {result}")
        logger.info(f"Result data: {result}")

        # The return value will be available in the SAQ context as ctx['result']
        # and should be stored in the database by the after_process hook
        return result

    except Exception as e:
        # Log the error
        logger.exception(f"Error in poc_test_task - job_id: {job_id}: {str(e)}")
        print(f"Error in poc_test_task - job_id: {job_id}: {str(e)}")
        # Re-raise the exception so SAQ marks the job as failed
        # This will be caught by SAQ and the error will be passed to after_process
        raise
