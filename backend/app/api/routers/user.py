# backend/app/api/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.db.session import get_db_session
from app.db.models import User
from app.schemas.user import UserProfile

# Define router prefix relative to /api if frontend proxy expects it
# Or adjust frontend apiService base URL if needed
router = APIRouter(prefix="/user", tags=["User"])  # Using /user prefix relative to /api


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    session: SessionContainer = Depends(verify_session()),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Get the profile information for the currently logged-in user.
    Fetches user based on SuperTokens session ID.
    """
    supertokens_user_id = session.get_user_id()
    stmt = select(User).where(User.supertokens_user_id == supertokens_user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        print(
            f"WARNING: Valid session for ST ID {supertokens_user_id} but no matching user in DB."
        )
        # It's crucial that the sign-up/sign-in overrides work correctly to prevent this.
        raise HTTPException(
            status_code=404, detail="User profile not found in database"
        )

    # Pydantic automatically maps matching attributes from User model to UserProfile schema
    # Ensure UserProfile schema fields match User model attributes (id, email)
    return user
