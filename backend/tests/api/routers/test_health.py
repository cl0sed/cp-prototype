"""
Tests for the health check endpoint.

This module contains integration tests for the /health endpoint,
which is responsible for providing API health status.
"""

from fastapi.testclient import TestClient


def test_health_check_succeeds(test_client: TestClient):
    """
    Test that the health check endpoint returns the expected response.

    This is an integration test using FastAPI's TestClient to make actual HTTP
    requests to the application. It verifies that:
    1. The endpoint returns a 200 status code
    2. The response has the correct content type
    3. The response body contains the expected JSON

    Unit tests for specific services/logic will be added separately in corresponding
    tests/ subdirectories (e.g., tests/features/).

    Future needs:
    - Mocking external services will require pytest-mock
    - Specific database testing strategies will be implemented later
    - This setup enables automated checks in the CI pipeline

    Args:
        test_client: The TestClient fixture injected from conftest.py
    """
    # Make a GET request to the /health endpoint
    response = test_client.get("/health")

    # Verify the response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


# To run: execute 'pytest' in the backend directory (or via Docker Compose)
