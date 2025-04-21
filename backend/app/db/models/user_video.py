from __future__ import annotations

from datetime import datetime
from uuid import UUID as PyUUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .video import Video


class UserVideo(Base):
    __tablename__ = "user_videos"

    user_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    video_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships to access the associated User and Video objects
    user: Mapped["User"] = relationship("User", back_populates="user_videos")
    video: Mapped["Video"] = relationship("Video", back_populates="user_videos")
