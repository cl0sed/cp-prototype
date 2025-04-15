"""
API Request/Response Data Schemas (Pydantic Models).

This file defines the data structures (shapes) for API request bodies and
response payloads using Pydantic models.

Define models that represent the exact data format expected by API endpoints
and returned to clients. Use FastAPI's integration with Pydantic for automatic
data validation and serialization.

Avoid putting database models (SQLAlchemy) or complex internal business objects
directly in API schemas. Keep them focused on the API contract.
Use distinct schemas for request input vs. response output if they differ significantly.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str
