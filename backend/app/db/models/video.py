from __future__ import annotations

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID as PyUUID

# from .user_video import UserVideo # Removed to break circular import
from .user import User
from .job import BackgroundJob

from sqlalchemy import (
    String,
    Text,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user_video import UserVideo
    from .user import User
    from .job import BackgroundJob


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True)
    creative_brief: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )

    # Relationships
    user_videos: Mapped[List["UserVideo"]] = relationship(
        "UserVideo", back_populates="video", cascade="all, delete-orphan"
    )
    users: Mapped[List["User"]] = relationship(
        "User", secondary="user_videos", viewonly=True
    )
    background_jobs: Mapped[List["BackgroundJob"]] = relationship(
        "BackgroundJob",
        foreign_keys="BackgroundJob.project_id",
        back_populates="video",
        cascade="all, delete-orphan",
    )
