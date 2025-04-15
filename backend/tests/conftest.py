"""
Test configuration and fixtures for the AI Video Creation Platform tests.

This file contains pytest fixtures that can be reused across multiple test files.
Fixtures defined here are automatically discovered by pytest without explicit imports.
"""

import pytest
from fastapi.testclient import TestClient
from typing import Iterator

from app.main import app


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
    with TestClient(app) as client:
        yield client


# To run: execute 'pytest' in the backend directory (or via Docker Compose)
