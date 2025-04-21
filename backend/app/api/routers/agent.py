"""
Agent interaction API endpoints.

This module contains routes for interacting with the AI agent.
These routes are protected by authentication.
"""

from fastapi import APIRouter
from pydantic import BaseModel


# Define a response model for the agent interaction
class AgentInteractionResponse(BaseModel):
    message: str
    user_email: str
    user_id: str


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)


# @router.get("/interact", response_model=AgentInteractionResponse)
# async def agent_interact(
#     user: User = Depends(get_required_user_from_session),
# ):
#     """
#     Test endpoint for agent interaction.
#     This endpoint is protected and requires authentication.

#     In a real implementation, this would handle the interaction with the AI agent.
#     """
#     # No need to check if user exists - the dependency handles that

#     # For now, just return a simple response
#     return AgentInteractionResponse(
#         message="Authentication successful",
#         user_email=user.email,
#         user_id=str(user.id),
#     )
