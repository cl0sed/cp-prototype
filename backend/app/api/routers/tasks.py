"""
Task Router Module.

This module defines the endpoints for triggering and managing background tasks.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.worker.settings import queue

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


class TriggerRequest(BaseModel):
    """Request model for the task trigger endpoint."""

    message: str = "Default message"
    user_id: Optional[uuid.UUID] = Field(
        default=None, description="User ID associated with this task"
    )
    project_id: Optional[uuid.UUID] = Field(
        default=None, description="Project ID associated with this task"
    )


class TriggerResponse(BaseModel):
    """Response model for the task trigger endpoint."""

    message: str
    job_id: str


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
    # Convert the Pydantic model to a dict, filtering out None values
    task_kwargs = {}
    for k, v in payload.dict().items():
        if v is not None:
            # Convert UUID objects to strings for JSON serialization
            if isinstance(v, uuid.UUID):
                task_kwargs[k] = str(v)
            else:
                task_kwargs[k] = v

    try:
        # Enqueue the task to be processed by the worker
        job = await queue.enqueue("poc_test_task", **task_kwargs)

        return TriggerResponse(
            message="Test task accepted and queued for processing", job_id=job.id
        )
    except Exception:
        # In a real application, you might want to log this error and handle it more gracefully
        # For now, just re-raise to let FastAPI handle it with a 500 error
        raise
