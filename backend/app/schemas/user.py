# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid  # Import uuid


class UserProfile(BaseModel):
    """
    Schema for returning user profile information.
    Reflects the User model structure.
    """

    id: uuid.UUID = Field(..., description="User's database primary key")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="User account creation timestamp")
    username: Optional[str] = Field(
        None, description="User's chosen username (optional)"
    )

    class Config:
        from_attributes = True  # For Pydantic v2+ compatibility with ORM models
