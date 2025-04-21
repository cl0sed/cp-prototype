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

    Args:
        ctx: The SAQ context object containing job information
        message: A test message to process
        user_id: Optional user ID associated with this task
        project_id: Optional project ID associated with this task

    Returns:
        A dictionary containing the job result
    """
    # Extract job ID and pipeline_tag from context for logging and tracking
    job = ctx.get("job")
    job_id = job.id if job else "unknown"
    # Access the pipeline_tag from the job object if needed for service/pipeline calls
    pipeline_tag = job.pipeline_tag if job else None
    logger.debug(f"DEBUG: Task {job_id} received pipeline_tag: {pipeline_tag}")

    logger.info(f"Starting poc_test_task - job_id: {job_id}, message: {message}")

    try:
        # Simulate work with a delay
        logger.info(f"Processing job {job_id} - simulating work...")
        await asyncio.sleep(2)

        # Process the message
        processed_message = f"Processed: {message}"

        # Create a result dictionary
        result = {
            "status": "success",
            "job_id": job_id,
            "processed_message": processed_message,
            "metadata": {
                "user_id": str(user_id) if user_id else None,
                "project_id": str(project_id) if project_id else None,
            },
        }

        logger.info(f"Completed poc_test_task - job_id: {job_id}")

        # Return result to be stored by after_process hook
        return result

    except Exception as e:
        # Log the error
        logger.exception(f"Error in poc_test_task - job_id: {job_id}: {str(e)}")
        # Re-raise to let SAQ handle the failure
        raise
