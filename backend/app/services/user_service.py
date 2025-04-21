import logging
from typing import List, cast
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db_session
from app.db.models.video import Video
from app.db.models.user_video import UserVideo

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for handling user-related operations, including fetching tasks.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_tasks(self, user_id: UUID) -> List[str]:
        """
        Fetches the titles of tasks assigned to a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of task titles (strings).
        """
        logger.info(f"Fetching tasks for user {user_id}")
        try:
            # Assuming tasks are represented by Videos
            # Query videos associated with the user through the association model
            query = (
                select(Video.title).join(UserVideo).filter(UserVideo.user_id == user_id)
            )
            result = await self.db.execute(query)
            tasks = result.scalars().all()
            logger.info(f"Found {len(tasks)} tasks for user {user_id}")
            return cast(List[str], tasks)
        except Exception as e:
            logger.error(f"Error fetching tasks for user {user_id}: {e}", exc_info=True)
            # Re-raise or handle as appropriate for the service layer
            raise e


# Dependency to get UserService instance
async def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    """
    FastAPI dependency to provide a UserService instance.
    """
    logger.debug("DEBUG: get_user_service dependency called")
    return UserService(db=db)
