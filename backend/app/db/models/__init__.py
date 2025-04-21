# Import all models to ensure they are registered with SQLAlchemy's metadata
from .base import Base
from .user import User
from .chat import ChatMessage
from .video import Video
from .user_video import UserVideo
from .job import BackgroundJob

# You can optionally define __all__ for explicit exports
__all__ = [
    "Base",
    "User",
    "ChatMessage",
    "Video",
    "UserVideo",
    "BackgroundJob",
]
