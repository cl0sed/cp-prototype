from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID as PyUUID

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .video import Video


class BackgroundJob(Base):
    __tablename__ = "background_jobs"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    job_type: Mapped[str] = mapped_column(
        String, nullable=False, index=True
    )  # e.g., 'ingest_content', 'generate_script', 'run_analysis'
    status: Mapped[str] = mapped_column(
        String, nullable=False, index=True
    )  # e.g., 'pending', 'running', 'completed', 'failed'
    project_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "videos.id", ondelete="CASCADE", use_alter=True
        ),  # Add use_alter=True
        nullable=True,
        index=True,
    )
    user_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    parameters: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default={}
    )  # Job-specific parameters
    result: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default={}
    )  # Job result/output
    error: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Error message if failed
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
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, index=True
    )

    # Relationships
    video: Mapped[Optional["Video"]] = relationship(
        "Video", back_populates="background_jobs"
    )
    initiating_user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="initiated_background_jobs"
    )
