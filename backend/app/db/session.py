"""
Database Session Management.

This file configures the SQLAlchemy engine and session handling.
It typically includes:
- Creating the database engine (connecting to the database).
- Defining a SessionLocal factory for creating new database sessions.
- Potentially providing a dependency (e.g., for FastAPI) to get a session
  scoped to a request.

Keep this focused on the mechanics of establishing and providing database
sessions. Avoid defining models or placing query logic here.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

# Create the AsyncEngine
# For local development, we use a simple configuration
# In production, connection pooling should be properly configured
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # SQL logging for development
    future=True,
    # Disable pooling for simplicity in development
    # For production, this should be properly configured
    poolclass=NullPool if settings.ENVIRONMENT == "development" else None,
)

# Create a configured "async_sessionmaker" factory
# This provides a factory that generates new AsyncSession instances
# when called, with the engine connection already established
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Define a FastAPI dependency to provide a session scoped to a request
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async SQLAlchemy session.

    Usage in FastAPI:
    ```
    @app.get("/items/")
    async def get_items(session: AsyncSession = Depends(get_db_session)):
        # Use session here
        pass
    ```

    This ensures that sessions are properly created and cleaned up for each request.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
