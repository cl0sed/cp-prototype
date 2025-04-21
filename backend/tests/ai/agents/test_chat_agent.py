import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Import the function to be tested
from app.ai.agents.chat_agent import build_chat_pipeline

# Import components that will be mocked

# Import dependencies that will be mocked
from app.services.prompt_service import PromptService
from app.config import Settings
from app.shared.exceptions import PromptTemplateNotFoundError


@pytest.fixture(autouse=True)
def mock_pipeline_dependencies():
    with (
        patch("app.ai.agents.chat_agent.PromptBuilder") as MockPromptBuilder,
        patch(
            "app.ai.agents.chat_agent.OpenAIChatGenerator"
        ) as MockOpenAIChatGenerator,
        patch("app.ai.agents.chat_agent.Agent") as MockAgent,
        patch("app.ai.agents.chat_agent.get_user_tasks_tool") as MockGetUserTasksTool,
        patch(
            "app.ai.agents.chat_agent.get_current_time_tool"
        ) as MockGetCurrentTimeTool,
    ):
        yield (
            MockPromptBuilder,
            MockOpenAIChatGenerator,
            MockAgent,
            MockGetUserTasksTool,
            MockGetCurrentTimeTool,
        )


@pytest.mark.asyncio
async def test_build_chat_pipeline_uses_prompt_service_and_settings(
    mock_pipeline_dependencies,
):
    # Unpack mocked components and tools
    (
        MockPromptBuilder,
        MockOpenAIChatGenerator,
        MockAgent,
        MockGetUserTasksTool,
        MockGetCurrentTimeTool,
    ) = mock_pipeline_dependencies

    # Create mock dependencies
    mock_prompt_service = AsyncMock(spec=PromptService)
    mock_settings = MagicMock(spec=Settings)

    # Configure mock_prompt_service to return dummy prompt content
    mock_prompt_service.get_prompt_template_content.side_effect = {
        ("chat", "main_prompt"): "Mock main prompt template",
        ("chat", "system_prompt"): "Mock system prompt template",
    }.get  # Use .get to return None for unexpected calls

    # Define test inputs
    test_pipeline_tag = "test_tag"

    # Call the function to build the pipeline
    pipeline = await build_chat_pipeline(
        pipeline_tag=test_pipeline_tag,
        prompt_service=mock_prompt_service,
        settings=mock_settings,
    )

    # Assert that PromptService methods were called with correct arguments
    mock_prompt_service.get_prompt_template_content.assert_any_call(
        pipeline_tag=test_pipeline_tag, prompt_name="main_prompt"
    )
    mock_prompt_service.get_prompt_template_content.assert_any_call(
        pipeline_tag=test_pipeline_tag, prompt_name="system_prompt"
    )

    # Assert that Haystack components were instantiated with expected values
    MockPromptBuilder.assert_called_once_with(template="Mock main prompt template")

    # Check Agent instantiation - it should receive the mocked generator and tools
    MockAgent.assert_called_once_with(
        chat_generator=MockOpenAIChatGenerator.return_value,  # Agent gets the instance returned by the mock
        tools=[
            MockGetUserTasksTool,
            MockGetCurrentTimeTool,
        ],  # Assert that the mocked tool functions are passed
        system_prompt="Mock system prompt template",
        exit_conditions=["text", "get_user_tasks"],
        max_agent_steps=10,
        raise_on_tool_invocation_failure=False,
    )

    # Check OpenAIChatGenerator instantiation - it should receive settings values
    MockOpenAIChatGenerator.assert_called_once_with(
        api_key=mock_settings.LLM_API_KEY,
        model=mock_settings.LLM_MODEL,
        api_base_url=mock_settings.LLM_API_URL if mock_settings.LLM_API_URL else None,
    )

    # Assert that the returned object is a Haystack AsyncPipeline (or a mock of it)
    # Since we mocked the components, the pipeline itself might be a mock or the real object
    # depending on how Haystack's AsyncPipeline is structured and if it's also mocked.
    # For now, we'll just check if something was returned.
    assert pipeline is not None
    # A more robust test might check the type if AsyncPipeline is not mocked,
    # or check if the mocked components were added to the pipeline mock if it is.


@pytest.mark.asyncio
async def test_build_chat_pipeline_raises_error_if_prompt_not_found(
    mock_pipeline_dependencies,
):
    # Unpack mocked components and tools
    (
        MockPromptBuilder,
        MockOpenAIChatGenerator,
        MockAgent,
        MockGetUserTasksTool,
        MockGetCurrentTimeTool,
    ) = mock_pipeline_dependencies

    # Create mock dependencies
    mock_prompt_service = AsyncMock(spec=PromptService)
    mock_settings = MagicMock(spec=Settings)

    # Configure mock_prompt_service to raise PromptTemplateNotFoundError
    mock_prompt_service.get_prompt_template_content.side_effect = (
        PromptTemplateNotFoundError("Mock prompt not found")
    )

    # Define test inputs
    test_pipeline_tag = "test_tag"

    # Expect PromptTemplateNotFoundError when building the pipeline
    with pytest.raises(PromptTemplateNotFoundError):
        await build_chat_pipeline(
            pipeline_tag=test_pipeline_tag,
            prompt_service=mock_prompt_service,
            settings=mock_settings,
        )

    # Verify that get_prompt_template_content was called (at least once before failing)
    mock_prompt_service.get_prompt_template_content.assert_called()


# Add more tests for different scenarios (e.g., different pipeline types) later
