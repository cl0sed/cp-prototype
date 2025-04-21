import pytest
from unittest.mock import AsyncMock, MagicMock

from haystack.core.pipeline import AsyncPipeline
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.agents import Agent
from haystack.utils import Secret  # Import Secret

from app.config import Settings
from app.services.prompt_service import PromptService
from app.ai.pipeline_builder import (
    build_chat_pipeline,
    chat_tools,
)  # Import chat_tools to check against
from app.shared.exceptions import PromptTemplateNotFoundError  # Import the exception


# Mock Settings object
@pytest.fixture
def mock_settings():
    settings = MagicMock(spec=Settings)
    settings.CHAT_PIPELINE_TAG = "chat_v1"
    settings.OPENAI_API_KEY = Secret.from_token("fake-api-key")  # Mock API key
    return settings


# Mock PromptService
@pytest.fixture
def mock_prompt_service():
    prompt_service = AsyncMock(spec=PromptService)
    # Configure the mock to return a dummy prompt template content
    prompt_service.get_prompt_template_content.return_value = (
        "Dummy prompt template: {chat_history}"
    )
    return prompt_service


# Mock AsyncSession
@pytest.fixture
def mock_async_session():
    return AsyncMock()


@pytest.mark.asyncio
async def test_build_chat_pipeline_success(
    mock_settings: Settings,
    mock_prompt_service: AsyncMock,
    mock_async_session: AsyncMock,
):
    """Test successful pipeline construction."""
    pipeline_tag = "chat_v1"

    pipeline = await build_chat_pipeline(
        pipeline_tag=pipeline_tag,
        prompt_service=mock_prompt_service,
        settings=mock_settings,
        db=mock_async_session,  # Pass the mock DB session
    )

    assert isinstance(pipeline, AsyncPipeline)
    # Assert that the 'agent' component exists in the pipeline
    assert pipeline.get_component("agent") is not None

    agent_component = pipeline.get_component("agent")
    assert isinstance(agent_component, Agent)

    # Verify Agent's chat_generator
    assert isinstance(agent_component.chat_generator, OpenAIChatGenerator)
    assert agent_component.chat_generator.api_key.resolve_value() == "fake-api-key"
    # Add assertions for other generator parameters if needed

    # Verify Agent's tools
    # Note: We are checking if the tools provided to the Agent are the same instances
    # as the ones imported from app.ai.tools
    assert agent_component.tools == chat_tools

    # Verify PromptService was called to fetch prompts
    mock_prompt_service.get_prompt_template_content.assert_any_call(
        db=mock_async_session,
        pipeline_tag=pipeline_tag,
        prompt_name="main_prompt",
    )
    mock_prompt_service.get_prompt_template_content.assert_any_call(
        db=mock_async_session,
        pipeline_tag=pipeline_tag,
        prompt_name="system_prompt",  # Check for system prompt fetch
    )
    # You can add checks for other prompt names if the builder fetches them

    # Verify Agent's system_prompt is set (assuming default or fetched)
    assert isinstance(agent_component.system_prompt, str)


@pytest.mark.asyncio
async def test_build_chat_pipeline_prompt_not_found(
    mock_settings: Settings,
    mock_prompt_service: AsyncMock,
    mock_async_session: AsyncMock,
):
    """Test pipeline construction when a prompt template is not found."""
    pipeline_tag = "chat_v1"

    # Configure mock PromptService to raise an exception
    mock_prompt_service.get_prompt_template_content.side_effect = (
        PromptTemplateNotFoundError("Prompt not found")
    )

    with pytest.raises(PromptTemplateNotFoundError):
        await build_chat_pipeline(
            pipeline_tag=pipeline_tag,
            prompt_service=mock_prompt_service,
            settings=mock_settings,
            db=mock_async_session,
        )

    # Verify PromptService was called
    mock_prompt_service.get_prompt_template_content.assert_any_call(
        db=mock_async_session,
        pipeline_tag=pipeline_tag,
        prompt_name="main_prompt",  # Or whichever prompt fetch fails first
    )
    # The pipeline should not be fully constructed if prompt fetching fails


# Add more tests for different scenarios if needed (e.g., different pipeline tags)
