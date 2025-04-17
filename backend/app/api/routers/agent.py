"""
Agent interaction API endpoints.

This module contains routes for interacting with the AI agent.
These routes are protected by authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from supertokens_python.recipe.session import SessionContainer

from app.db.session import get_db_session
from app.features.auth import session_verifier, get_user_from_session

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)


@router.get("/interact", response_model=dict)
async def agent_interact(
    session: SessionContainer = Depends(session_verifier),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Test endpoint for agent interaction.
    This endpoint is protected and requires authentication.

    In a real implementation, this would handle the interaction with the AI agent.
    """
    # Get the user from the session
    user = await get_user_from_session(session, db)

    if not user:
        raise HTTPException(
            status_code=403,
            detail="User not found in database",
        )

    # For now, just return a simple response
    return {
        "message": "Authentication successful",
        "user_email": user.email,
        "user_id": str(user.id),
    }
