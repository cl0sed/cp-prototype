# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid  # Import uuid


class UserProfile(BaseModel):
    """
    Schema for returning user profile information.
    Reflects the User model structure.
    """

    id: uuid.UUID = Field(..., description="User's database primary key")
    email: EmailStr = Field(..., description="User's email address")
    created_at: datetime = Field(..., description="User account creation timestamp")
    # Username is omitted as it's not in the User model

    class Config:
        from_attributes = True  # For Pydantic v2+ compatibility with ORM models
