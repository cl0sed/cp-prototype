from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    TIMESTAMP,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    metadata_: Mapped[dict] = mapped_column(JSONB, nullable=False, default={})

    __table_args__ = (
        Index("ix_chat_message_session_timestamp", "session_id", "timestamp"),
        Index("ix_chat_message_user_timestamp", "user_id", "timestamp"),
    )
