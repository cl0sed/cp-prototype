import logging
from typing import Optional
import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.db.models.user import User
from app.features.auth import get_required_user_from_session
from app.services.chat_service import ChatService, get_chat_service

# Import schemas and dependencies from the new feature-specific files
from app.features.chat.schemas import (
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatMessageRequest,
    ChatMessageAPIResponse,
    GreetingResponse,
)

logger = logging.getLogger(__name__)

# --- Router ---

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)

# --- Endpoints ---


@router.get("/greeting", response_model=GreetingResponse)
async def get_greeting(
    user_id: UUID = Depends(
        get_required_user_from_session
    ),  # Accept user_id instead of User object
    db: AsyncSession = Depends(get_db_session),  # Inject DB session
    chat_service: ChatService = Depends(get_chat_service),  # Inject ChatService
):
    """
    Generates a dynamic greeting for the authenticated user based on past interactions.
    """
    logger.info(f"Generating dynamic greeting for user {user_id}.")

    try:
        # Call the new service method to generate the greeting
        greeting_text = await chat_service.generate_greeting(db=db, user_id=user_id)

        return GreetingResponse(greeting=greeting_text)

    except Exception as e:
        logger.error(
            f"ERROR: Exception during greeting generation for user {user_id}: {e}",
            exc_info=True,
        )
        # Re-raise as HTTPException or handle as appropriate for the router layer
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate greeting.",
        ) from e


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: UUID = Depends(
        get_required_user_from_session
    ),  # Accept user_id instead of User object
    db: AsyncSession = Depends(get_db_session),
    chat_service: ChatService = Depends(get_chat_service),  # Inject ChatService
    session_id: Optional[UUID] = None,  # Optional query parameter
    limit: int = Query(default=5, ge=1, le=10),  # Optional limit query parameter
):
    """
    Retrieves chat message history for the authenticated user.
    Can filter by session_id or retrieve recent messages across sessions.
    """
    logger.info(
        f"Fetching chat history for user {user_id}, session_id: {session_id}, limit: {limit}"
    )

    try:
        # Call the new service method to get chat history
        messages = await chat_service.get_history(
            db=db, user_id=user_id, session_id=session_id, limit=limit
        )

        # Convert ORM models to Pydantic models
        chat_messages_response = [
            ChatMessageResponse.model_validate(msg) for msg in messages
        ]

        logger.info(f"Found {len(messages)} chat messages for user {user_id}")
        return ChatHistoryResponse(messages=chat_messages_response)

    except Exception as e:
        logger.error(
            f"Failed to fetch chat history for user {user_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history.",
        ) from e


@router.post("/message", response_model=ChatMessageAPIResponse)
async def post_chat_message(
    request: ChatMessageRequest,
    user_id: UUID = Depends(get_required_user_from_session),
    db: AsyncSession = Depends(get_db_session),
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Processes a new user chat message, interacts with the AI agent, and returns the response.
    Manages chat sessions.
    """
    logger.info(
        f"Received message for user {user_id}, session_id: {request.session_id}"
    )

    # Use the provided session_id or generate a new one
    session_id_str = (
        str(request.session_id) if request.session_id else str(uuid.uuid4())
    )

    # Interact with the ChatService
    try:
        # Fetch User object as ChatService.interact expects it
        user = await db.get(User, user_id)
        if not user:
            # This case should ideally not happen if get_required_user_from_session works correctly,
            # but handle defensively.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        response = await chat_service.interact(
            db=db,
            user_message=request.message,  # Pass the simple string message
            user=user,  # Pass the fetched User object
            session_id=session_id_str,  # Pass the generated session ID
        )
        # ChatService.interact returns {"reply": str, "session_id": str}
        return ChatMessageAPIResponse(
            reply=response["reply"], session_id=UUID(response["session_id"])
        )
    except HTTPException as e:
        # Re-raise HTTPExceptions from the service layer
        raise e
    except Exception as e:
        logger.error(
            f"Error processing chat message for user {user_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message.",
        ) from e
