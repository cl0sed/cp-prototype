from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID as PyUUID

# from .user_video import UserVideo # Removed to break circular import
# from .video import Video # Removed to break circular import
# from .job import BackgroundJob # Removed to break circular import

from sqlalchemy import (
    String,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user_video import UserVideo
    from .video import Video
    from .job import BackgroundJob


class User(Base):
    __tablename__ = "users"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    supertokens_user_id: Mapped[Optional[str]] = mapped_column(
        String, unique=True, index=True, nullable=True
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(
        String, nullable=False, default="user", index=True
    )

    # Relationships
    user_videos: Mapped[List["UserVideo"]] = relationship(
        "UserVideo", back_populates="user", cascade="all, delete-orphan"
    )
    videos: Mapped[List["Video"]] = relationship(
        "Video", secondary="user_videos", viewonly=True
    )
    initiated_background_jobs: Mapped[List["BackgroundJob"]] = relationship(
        "BackgroundJob",
        foreign_keys="BackgroundJob.user_id",
        back_populates="initiating_user",
    )
