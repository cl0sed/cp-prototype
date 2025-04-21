"""
Health check router module.

This module defines the health check endpoint to verify API operational status.
"""

from fastapi import APIRouter, Depends  # type: ignore
from ..schemas import HealthResponse
from app.config import (
    Settings,
    get_settings,
)  # Import Settings and the cached dependency

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify API is running.
    Returns a simple response with status "ok".
    """
    return HealthResponse(status="ok")


@router.get("/test-settings")
async def test_settings_dependency(settings: Settings = Depends(get_settings)):
    """
    Temporary endpoint to test Settings dependency injection.
    """
    # Return a simple confirmation or a setting value
    return {
        "status": "Settings dependency injected successfully",
        "log_level": settings.LOG_LEVEL,
    }
