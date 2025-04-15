"""
Health check router module.

This module defines the health check endpoint to verify API operational status.
"""

from fastapi import APIRouter  # type: ignore
from ..schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify API is running.
    Returns a simple response with status "ok".
    """
    return HealthResponse(status="ok")
