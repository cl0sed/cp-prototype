"""
Test configuration and fixtures for the AI Video Creation Platform tests.

This file contains pytest fixtures that can be reused across multiple test files.
Fixtures defined here are automatically discovered by pytest without explicit imports.
"""

import pytest
from unittest.mock import MagicMock, patch  # Import MagicMock and patch
import uuid  # Import uuid
from .factories import SettingsFactory  # Import SettingsFactory
from fastapi.testclient import TestClient
from typing import Iterator
from app.main import app  # Import app after patching Settings
from app.db.models import User  # Import User model
from app.features.auth import (
    init_supertokens,
    get_required_user_from_session,
)  # Import SuperTokens initialization and the dependency function


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.base import Base  # Import Base from the new location

# Setup for test database
# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use a file-based SQLite for persistence across tests if needed, or :memory: for in-memory
# For in-memory: SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a transactional database session for tests.

    A new session is created for each test function, and all changes are rolled back
    after the test completes to ensure test isolation.
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the database tables after each test function
        Base.metadata.drop_all(bind=engine)


# Patch app.config.Settings before importing app.main or any module that imports app.config
# This intercepts the Settings() call that happens at module level in app.config
# Configure the patched Settings class to return a Settings instance built by SettingsFactory when called.
# This ensures that any code calling Settings() during the import phase gets a valid, factory-built object.
patch_settings_class = patch("app.config.Settings")
MockSettingsClass = patch_settings_class.start()

MockSettingsClass.return_value = SettingsFactory.build()


@pytest.fixture(scope="module")
def test_client() -> Iterator[TestClient]:
    """
    Provides a FastAPI TestClient instance scoped for a module.

    This fixture creates a TestClient that can be used to make requests to the FastAPI
    application. The module scope means setup runs once per test module, making it
    efficient for stateless clients.

    The TestClient automatically handles application startup/shutdown lifespan events.

    Future shared fixtures (e.g., DB connections, mocks) will also reside in this file.

    Returns:
        Iterator[TestClient]: A TestClient instance for making requests to the app.
    """
    # Create a mock user object
    mock_user = MagicMock(spec=User)
    mock_user.id = uuid.uuid4()
    mock_user.email = "testuser@example.com"
    mock_user.role = "user"

    # Initialize SuperTokens for the test app instance
    init_supertokens(app)

    # Override the authentication dependency to return the mock user
    app.dependency_overrides[get_required_user_from_session] = lambda: mock_user

    with TestClient(app, cookies={"sAccessToken": "dummy_token"}) as client:
        yield client

    # Clean up dependency overrides after the test
    app.dependency_overrides.clear()


# To run: execute 'pytest' in the backend directory (or via Docker Compose)

# The mock_app_settings fixture is now redundant as Settings is patched.
# Removing it.
