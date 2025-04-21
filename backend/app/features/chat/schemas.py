from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime  # Import datetime

from pydantic import BaseModel, Field

# --- Chat Pydantic Models ---


class ChatMessageResponse(BaseModel):
    """Represents a single chat message in the API response."""

    id: UUID
    session_id: UUID  # Change type to UUID
    role: str  # 'user', 'assistant', 'tool'
    content: str
    timestamp: datetime  # Change type to datetime
    metadata_: Dict[str, Any] = {}  # Renamed to avoid conflict with Python keyword

    class Config:
        from_attributes = True  # Enable ORM mode


class ChatHistoryResponse(BaseModel):
    """Represents a list of chat messages for a session or user."""

    messages: List[ChatMessageResponse]


class ChatMessageRequest(BaseModel):
    """Represents the request body for sending a new message."""

    message: str
    session_id: Optional[UUID] = Field(
        None, description="Optional session ID to continue a conversation"
    )  # Explicitly use Field for default


class ChatMessageAPIResponse(BaseModel):
    """Represents the response body after sending a message."""

    reply: str
    session_id: UUID


class GreetingResponse(BaseModel):
    """Represents the response for the greeting endpoint."""

    greeting: str
    # Potentially add user-specific info here, e.g., recent tasks summary
