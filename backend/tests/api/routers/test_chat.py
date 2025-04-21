import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
import uuid

from tests.factories import UserFactory, ChatMessageFactory  # Import factories

# Import app and the dependency to override
from app.main import app
from app.services.prompt_service import PromptService
from app.config import Settings
from pydantic import SecretStr
from app.services.chat_service import ChatService  # Import the actual service

# --- Fixtures providing mock objects ---


@pytest.fixture
def mock_user_obj():
    """Provides a mock User object using UserFactory."""
    # Use the factory to create a mock user object
    return UserFactory.build(role="user")


@pytest.fixture
def mock_async_session_obj():
    """Provides a mock AsyncSession object with execute mocked."""
    session = AsyncMock()
    session.execute = AsyncMock()  # Mock the execute method itself
    return session


@pytest.fixture
def mock_settings_obj():
    """Provides a mock Settings object."""
    settings = MagicMock(spec=Settings)
    settings.CHAT_PIPELINE_TAG = "chat_v1"
    settings.OPENAI_API_KEY = SecretStr("fake-api-key")
    settings.PROMPT_CONFIG = {
        "pipelines": {
            "chat_v1": {
                "greeting_prompt": {"name": "chat_greeting", "version": "1.0"},
                "main_prompt": {"name": "chat_main", "version": "1.0"},
                "system_prompt": {"name": "chat_system", "version": "1.0"},
            }
        }
    }
    return settings


@pytest.fixture
def mock_prompt_service_obj(mock_settings_obj: MagicMock):
    """Provides a mock PromptService object."""
    prompt_service = AsyncMock(spec=PromptService)
    # Configure mock to return dummy prompt content for greeting and main prompts
    prompt_service.get_prompt_template_content.side_effect = (
        lambda db, pipeline_tag, prompt_name: {
            "greeting_prompt": "Hello, {username}!",
            "main_prompt": "Chat history: {chat_history}\nUser: {user_message}\nAgent:",
            "system_prompt": "You are a helpful assistant.",
        }.get(prompt_name, f"Dummy {prompt_name} content")
    )
    return prompt_service


@pytest.fixture
def mock_chat_service_obj(
    mock_settings_obj: MagicMock, mock_prompt_service_obj: AsyncMock
):
    """Provides a mock ChatService object."""
    chat_service = AsyncMock(spec=ChatService)
    chat_service.interact.return_value = {
        "reply": "Mocked agent response",
        "session_id": str(uuid.uuid4()),
    }
    return chat_service


# --- Integration tests for /api/chat endpoints ---


@pytest.mark.asyncio
async def test_get_greeting_endpoint(
    mocker,  # Add mocker fixture
    test_client: TestClient,  # The actual test client
    # Inject fixture results (the mock objects)
    mock_user_obj: MagicMock,
    mock_prompt_service_obj: AsyncMock,
    mock_chat_service_obj: AsyncMock,
    mock_settings_obj: MagicMock,
    mock_async_session_obj: AsyncMock,
):
    """Test the GET /api/chat/greeting endpoint."""
    # Configure patched dependencies to return the fixture results (the mock objects)
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").return_value = mock_user_obj
    # Override DB session dependency
    mocker.patch("app.db.session.get_db_session").return_value = mock_async_session_obj
    mocker.patch(
        "app.services.prompt_service.get_prompt_service"
    ).return_value = mock_prompt_service_obj
    mocker.patch("app.config.Settings").return_value = mock_settings_obj
    mocker.patch(
        "app.services.chat_service.get_chat_service"
    ).return_value = mock_chat_service_obj

    response = test_client.get("/api/chat/greeting")
    app.dependency_overrides.clear()  # Clean up override

    assert response.status_code == 200
    assert "greeting" in response.json()
    assert response.json()["greeting"] == f"Hello, {mock_user_obj.email}!"

    # Verify patched dependency mocks were called
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").assert_called_once()
    mocker.patch("app.db.session.get_db_session").assert_called_once()
    mocker.patch("app.services.prompt_service.get_prompt_service").assert_called_once()
    mocker.patch("app.config.Settings").assert_called_once()
    mocker.patch("app.services.chat_service.get_chat_service").assert_called_once()


@pytest.mark.asyncio
async def test_post_chat_message_endpoint_new_session(
    mocker,  # Add mocker fixture
    test_client: TestClient,  # The actual test client
    # Inject fixture results (the mock objects)
    mock_user_obj: MagicMock,
    mock_chat_service_obj: AsyncMock,
    mock_async_session_obj: AsyncMock,
):
    """Test the POST /api/chat/message endpoint for a new session."""
    # Configure patched dependencies to return the fixture results (the mock objects)
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").return_value = mock_user_obj
    # Override DB session dependency
    mocker.patch("app.db.session.get_db_session").return_value = mock_async_session_obj
    mocker.patch(
        "app.services.chat_service.get_chat_service"
    ).return_value = mock_chat_service_obj

    user_message = "Hello AI!"
    request_body = {"message": user_message}  # No session_id for a new session

    response = test_client.post("/api/chat/message", json=request_body)
    app.dependency_overrides.clear()  # Clean up override

    assert response.status_code == 200
    assert "reply" in response.json()
    assert "session_id" in response.json()

    # Verify ChatService.interact was called with the correct arguments on the mock object
    mock_chat_service_obj.interact.assert_called_once()
    call_args, call_kwargs = mock_chat_service_obj.interact.call_args
    assert call_kwargs["db"] == mock_async_session_obj
    assert call_kwargs["user_message"] == user_message
    assert call_kwargs["user"] == mock_user_obj
    assert isinstance(
        uuid.UUID(call_kwargs["session_id"]), uuid.UUID
    )  # Check if session_id is a valid UUID string

    # Verify patched dependency mocks were called
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").assert_called_once()
    mocker.patch("app.db.session.get_db_session").assert_called_once()
    mocker.patch("app.services.chat_service.get_chat_service").assert_called_once()


@pytest.mark.asyncio
async def test_post_chat_message_endpoint_existing_session(
    mocker,  # Add mocker fixture
    test_client: TestClient,  # The actual test client
    # Inject fixture results (the mock objects)
    mock_user_obj: MagicMock,
    mock_chat_service_obj: AsyncMock,
    mock_async_session_obj: AsyncMock,
):
    """Test the POST /api/chat/message endpoint for an existing session."""
    # Configure patched dependencies to return the fixture results (the mock objects)
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").return_value = mock_user_obj
    # Override DB session dependency
    mocker.patch("app.db.session.get_db_session").return_value = mock_async_session_obj
    mocker.patch(
        "app.services.chat_service.get_chat_service"
    ).return_value = mock_chat_service_obj

    user_message = "Tell me more."
    existing_session_id = str(uuid.uuid4())
    request_body = {
        "message": user_message,
        "session_id": existing_session_id,
    }  # Existing session_id

    response = test_client.post("/api/chat/message", json=request_body)
    app.dependency_overrides.clear()  # Clean up override

    assert response.status_code == 200
    assert "reply" in response.json()
    assert "session_id" in response.json()
    assert (
        response.json()["session_id"] == existing_session_id
    )  # Response should return the same session_id

    # Verify ChatService.interact was called with the correct arguments on the mock object
    mock_chat_service_obj.interact.assert_called_once()
    call_args, call_kwargs = mock_chat_service_obj.interact.call_args
    assert call_kwargs["db"] == mock_async_session_obj
    assert call_kwargs["user_message"] == user_message
    assert call_kwargs["user"] == mock_user_obj
    assert (
        call_kwargs["session_id"] == existing_session_id
    )  # Should pass the existing session_id

    # Verify patched dependency mocks were called
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").assert_called_once()
    mocker.patch("app.db.session.get_db_session").assert_called_once()
    mocker.patch("app.services.chat_service.get_chat_service").assert_called_once()


@pytest.mark.asyncio
async def test_get_chat_history_endpoint_with_session_id(
    mocker,  # Add mocker fixture
    test_client: TestClient,  # The actual test client
    # Inject fixture results (the mock objects)
    mock_user_obj: MagicMock,
    mock_async_session_obj: AsyncMock,
):
    """Test the GET /api/chat/history endpoint with a session_id."""
    # Configure patched dependencies to return the fixture results (the mock objects)
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").return_value = mock_user_obj
    # Override DB session dependency
    mocker.patch("app.db.session.get_db_session").return_value = mock_async_session_obj

    # Mock the database query result for ChatMessage history using ChatMessageFactory
    mock_messages = ChatMessageFactory.build_batch(
        2,
        user_id=mock_user_obj.id,
        session_id=uuid.uuid4(),  # Use a single session_id for these messages
    )
    # Optionally, customize content or roles if needed for specific test cases
    mock_messages[0].role = "user"
    mock_messages[0].content = "Hi"
    mock_messages[1].role = "assistant"
    mock_messages[1].content = "Hello"
    # Configure the awaitable result of execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_messages
    mock_async_session_obj.execute.return_value = (
        mock_result  # Set the awaitable's result
    )

    session_id = uuid.uuid4()
    response = test_client.get(f"/api/chat/history?session_id={session_id}")
    app.dependency_overrides.clear()  # Clean up override

    assert response.status_code == 200
    assert "messages" in response.json()
    assert len(response.json()["messages"]) == len(mock_messages)
    # Add assertions to check the structure and content of returned messages if needed

    # Verify the database query was executed correctly on the mock object
    mock_async_session_obj.execute.assert_called_once()
    # You can add more specific assertions about the select statement filtering by session_id

    # Verify patched dependency mocks were called
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").assert_called_once()
    mocker.patch("app.db.session.get_db_session").assert_called_once()
    # Note: ChatService is not directly involved in this endpoint's logic


@pytest.mark.asyncio
async def test_get_chat_history_endpoint_recent_messages(
    mocker,  # Add mocker fixture
    test_client: TestClient,  # The actual test client
    # Inject fixture results (the mock objects)
    mock_user_obj: MagicMock,
    mock_async_session_obj: AsyncMock,
):
    """Test the GET /api/chat/history endpoint for recent messages across sessions."""
    # Configure patched dependencies to return the fixture results (the mock objects)
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").return_value = mock_user_obj
    # Override DB session dependency
    mocker.patch("app.db.session.get_db_session").return_value = mock_async_session_obj

    # Mock the database query result for recent ChatMessage history using ChatMessageFactory
    # Create messages from different sessions
    mock_messages = [
        ChatMessageFactory.build(
            user_id=mock_user_obj.id,
            session_id=uuid.uuid4(),
            role="user",
            content="Hi 2",
        ),
        ChatMessageFactory.build(
            user_id=mock_user_obj.id,
            session_id=uuid.uuid4(),
            role="assistant",
            content="Hello 1",
        ),
    ]
    # Ensure timestamps are different for ordering tests if necessary, or rely on factory default
    # Configure the awaitable result of execute
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_messages
    mock_async_session_obj.execute.return_value = (
        mock_result  # Set the awaitable's result
    )

    response = test_client.get("/api/chat/history")  # No session_id
    app.dependency_overrides.clear()  # Clean up override

    assert response.status_code == 200
    assert "messages" in response.json()
    assert len(response.json()["messages"]) == len(mock_messages)
    # Add assertions to check the structure and content of returned messages if needed
    # Note: The response should have messages in chronological order (reversed from DB query)

    # Verify the database query was executed correctly on the mock object
    mock_async_session_obj.execute.assert_called_once()
    # You can add more specific assertions about the select statement ordering and limit

    # Verify patched dependency mocks were called
    # Handled by conftest override: mocker.patch("app.features.auth.get_required_user_from_session").assert_called_once()
    mocker.patch("app.db.session.get_db_session").assert_called_once()
    # Note: ChatService is not directly involved in this endpoint's logic
