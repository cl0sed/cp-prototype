"""
Task Router Module.

This module defines the endpoints for triggering and managing background tasks.
"""

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.worker.settings import queue
from app.shared.constants.constants import (
    Status as JobStatus,
)  # Import SAQ's Status enum directly

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


class TriggerRequest(BaseModel):
    """Request model for the task trigger endpoint."""

    message: str = Field(default="Default message", description="Message to process")
    user_id: Optional[uuid.UUID] = Field(
        default=None, description="User ID associated with this task"
    )
    video_id: Optional[uuid.UUID] = Field(
        default=None, description="Video ID associated with this task"
    )


class TriggerResponse(BaseModel):
    """Response model for the task trigger endpoint."""

    message: str
    job_id: str
    status: str


@router.post(
    "/trigger-test",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TriggerResponse,
)
async def trigger_test_task(payload: TriggerRequest) -> TriggerResponse:
    """
    Trigger a test background task using SAQ.

    This endpoint demonstrates how to enqueue a background task and return immediately.
    The task will be processed asynchronously by the worker.

    Returns:
        A response containing the job ID that can be used to track the task's status.
    """
    # Safely handle UUID objects for JSON serialization
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
            message="Test task accepted and queued for processing",
            job_id=job.id,
            status=JobStatus.QUEUED.value,  # Use the native SAQ status value
        )
    except Exception as e:
        # Log and handle any enqueue errors
        logger.exception(f"Failed to enqueue task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enqueue task: {str(e)}",
        )
