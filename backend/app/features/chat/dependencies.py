import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.db.session import get_db_session  # Assuming this dependency exists
from app.services.prompt_service import (
    PromptService,
    get_prompt_service,
)  # Import PromptService and its dependency
from app.features.chat.chat_pipeline import (
    build_chat_pipeline,
)  # Import pipeline builder from new location

logger = logging.getLogger(__name__)


# Dependency to get the chat pipeline (built per request to include DB session)
async def get_chat_pipeline(
    settings: Settings,
    prompt_service: PromptService = Depends(get_prompt_service),  # Inject PromptService
    db: AsyncSession = Depends(
        get_db_session
    ),  # Keep DB session dependency for now as it's passed to pipeline builder
):
    """FastAPI dependency to provide a configured chat pipeline."""
    try:
        # Build the pipeline using the builder function
        # Pass override_pipeline_tag=None for API calls using the default tag
        pipeline = await build_chat_pipeline(
            pipeline_type="chat",  # Specify pipeline type
            override_pipeline_tag=None,  # Use default tag for API calls
            prompt_service=prompt_service,
            settings=settings,
            db=db,  # Pass db argument as it's needed by the pipeline builder
        )
        return pipeline
    except Exception as e:
        logger.error(f"Failed to build chat pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize chat pipeline.",
        ) from e
