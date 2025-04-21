from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.db.models.user import User
from app.api.schemas import UserProfile
from app.features.auth import (
    get_user_from_session,
)  # Added import for get_user_from_session

# Define router prefix relative to /api if frontend proxy expects it
# Or adjust frontend apiService base URL if needed
router = APIRouter(prefix="/user", tags=["User"])  # Using /user prefix relative to /api


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    user: Optional[User] = Depends(
        get_user_from_session
    ),  # Use the dependency instead of manual fetching
):
    """
    Get the profile information for the currently logged-in user.
    Uses get_user_from_session dependency to fetch user based on SuperTokens session ID.
    """
    if not user:
        # Standardized to use 403 Forbidden for consistency with other endpoints
        raise HTTPException(
            status_code=403, detail="User profile not found in database"
        )

    # Pydantic automatically maps matching attributes from User model to UserProfile schema
    # Ensure UserProfile schema fields match User model attributes (id, email)
    return user
