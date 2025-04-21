import pytest
import datetime
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.tools import get_current_time_tool_func, get_user_tasks_tool_func
from app.db.models import User  # Import User and Video models for mocking


# Mock User object
@pytest.fixture
def mock_user():
    user = MagicMock(spec=User)
    user.id = uuid.uuid4()
    user.role = "user"  # Default role
    return user


# Mock Admin User object
@pytest.fixture
def mock_admin_user():
    admin_user = MagicMock(spec=User)
    admin_user.id = uuid.uuid4()
    admin_user.role = "admin"  # Admin role
    return admin_user


# Mock AsyncSession
@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)


# Unit tests for get_current_time_tool_func
@pytest.mark.asyncio
async def test_get_current_time_tool_func():
    """Test the get_current_time tool function."""
    result = get_current_time_tool_func()  # Removed await

    assert "current_time" in result
    # Basic check if the output is a string and looks like a timestamp
    assert isinstance(result["current_time"], str)
    try:
        datetime.datetime.fromisoformat(result["current_time"])
    except ValueError:
        pytest.fail("Output 'current_time' is not in ISO format")


# Unit tests for get_user_tasks_tool_func
@pytest.mark.asyncio
async def test_get_user_tasks_tool_func_current_user(
    mock_user: MagicMock, mock_async_session: AsyncMock
):
    """Test get_user_tasks tool for the current user."""
    mock_tasks = ["Task A", "Task B"]
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = mock_tasks  # Mock the result of the query

    mock_async_session.execute.return_value = mock_result  # Mock the execute method

    state = {"user": mock_user, "db": mock_async_session}
    kwargs = {}  # No user_id specified, should use user from state

    result = await get_user_tasks_tool_func(
        state=state, **kwargs
    )  # Await the async function

    assert "tasks" in result
    assert result["tasks"] == mock_tasks
    # Verify the database query was executed with the correct user_id
    mock_async_session.execute.assert_called_once()
    # You can add more specific assertions about the select statement if needed


@pytest.mark.asyncio
async def test_get_user_tasks_tool_func_admin_other_user(
    mock_admin_user: MagicMock, mock_user: MagicMock, mock_async_session: AsyncMock
):
    """Test get_user_tasks tool for an admin requesting another user's tasks."""
    mock_tasks = ["Other User Task 1", "Other User Task 2"]
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = mock_tasks

    mock_async_session.execute.return_value = mock_result

    state = {"user": mock_admin_user, "db": mock_async_session}
    kwargs = {"user_id": str(mock_user.id)}  # Admin requests another user's tasks

    result = await get_user_tasks_tool_func(state=state, **kwargs)

    assert "tasks" in result
    assert result["tasks"] == mock_tasks
    # Verify the database query was executed with the target user_id
    mock_async_session.execute.assert_called_once()
    # You can add more specific assertions about the select statement filtering by mock_user.id


@pytest.mark.asyncio
async def test_get_user_tasks_tool_func_non_admin_other_user(
    mock_user: MagicMock, mock_async_session: AsyncMock
):
    """Test get_user_tasks tool for a non-admin requesting another user's tasks (should fail)."""
    other_user_id = uuid.uuid4()  # A different user ID

    state = {"user": mock_user, "db": mock_async_session}
    kwargs = {"user_id": str(other_user_id)}  # Non-admin requests another user's tasks

    result = await get_user_tasks_tool_func(state=state, **kwargs)

    assert "error" in result
    assert "permission" in result["error"]
    # Verify that the database was NOT queried
    mock_async_session.execute.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_tasks_tool_func_db_error(
    mock_user: MagicMock, mock_async_session: AsyncMock
):
    """Test get_user_tasks tool when a database error occurs."""
    mock_async_session.execute.side_effect = Exception(
        "Database connection failed"
    )  # Simulate DB error

    state = {"user": mock_user, "db": mock_async_session}
    kwargs = {}  # Current user

    result = await get_user_tasks_tool_func(state=state, **kwargs)

    assert "error" in result
    assert "Failed to retrieve tasks" in result["error"]
    # Verify the database query was attempted
    mock_async_session.execute.assert_called_once()
