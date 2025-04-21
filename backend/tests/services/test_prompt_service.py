import pytest
import yaml
import os
from unittest.mock import MagicMock, patch, AsyncMock  # Added patch, AsyncMock

from app.services.prompt_service import PromptService
from app.config import Settings  # Assuming Settings is importable like this
from app.lifecycle import lifespan  # Added lifespan
from fastapi import FastAPI  # Added FastAPI


# Define a fixture for creating mock settings
@pytest.fixture
def mock_settings(tmp_path):
    """Provides mock Settings with a temporary config file path and dummy prompt files."""
    # Create dummy config file
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "pipeline-tags.yaml"

    dummy_config_content = {
        "stable": {"chat": {"system": "v1", "main_chat": "v1"}},
        "experimental": {"chat": {"system": "v2"}},
    }
    with open(config_path, "w") as f:
        yaml.dump(dummy_config_content, f)

    # Create dummy prompt files mimicking the app structure
    # Structure: app/features/chat/prompts/{name}/{version}.j2
    prompt_base_dir = tmp_path / "app" / "features" / "chat" / "prompts"
    prompt_base_dir.mkdir(parents=True)

    # stable/chat prompts
    (prompt_base_dir / "system").mkdir()
    (prompt_base_dir / "system" / "v1.j2").write_text("System prompt v1 content")
    (prompt_base_dir / "main_chat").mkdir()
    (prompt_base_dir / "main_chat" / "v1.j2").write_text("Main chat prompt v1 content")

    # experimental/chat prompts
    (prompt_base_dir / "system" / "v2.j2").write_text("System prompt v2 content")

    # Fallback prompt
    # Assuming fallback prompts might live in shared or a specific fallback location
    # For simplicity, let's put a fallback version in the same structure for now
    # A more robust test might involve a separate shared/prompts structure
    (prompt_base_dir / "fallback_prompt").mkdir()
    (prompt_base_dir / "fallback_prompt" / "v1_fallback.j2").write_text(
        "Fallback prompt content"
    )

    settings = MagicMock(spec=Settings)
    settings.PIPELINE_TAGS_CONFIG_PATH = str(config_path)
    settings.DEFAULT_PROMPT_VERSION = "v1_fallback"  # Default fallback version
    settings.DEFAULT_CHAT_PIPELINE_TAG = "stable"  # Default chat tag
    # Add other default tags as needed for future tests
    # settings.DEFAULT_OTHER_PIPELINE_TAG = "default_other_tag"

    # Mock os.getcwd() to return tmp_path so PromptService can find the dummy files
    original_getcwd = os.getcwd
    os.getcwd = lambda: str(tmp_path)
    yield settings, dummy_config_content, tmp_path  # Use yield for teardown

    # Restore original os.getcwd() after the test
    os.getcwd = original_getcwd


# Test for successful configuration loading
def test_prompt_service_init_loads_config(mock_settings):
    settings, expected_config, _ = mock_settings

    service = PromptService(settings)

    assert service.pipeline_tags_config_ == expected_config


# Test for missing configuration file
def test_prompt_service_init_missing_config(tmp_path):
    settings = MagicMock(spec=Settings)
    settings.PIPELINE_TAGS_CONFIG_PATH = str(tmp_path / "non_existent_config.yaml")
    settings.DEFAULT_PROMPT_VERSION = "v1_fallback"
    settings.DEFAULT_CHAT_PIPELINE_TAG = "stable"

    service = PromptService(settings)

    assert service.pipeline_tags_config_ == {}  # Should load as empty dict


# Test for invalid YAML configuration file
def test_prompt_service_init_invalid_yaml(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "invalid-config.yaml"

    # Create an invalid YAML file
    invalid_yaml_content = "key: [ - invalid_list"
    with open(config_path, "w") as f:
        f.write(invalid_yaml_content)

    settings = MagicMock(spec=Settings)
    settings.PIPELINE_TAGS_CONFIG_PATH = str(config_path)
    settings.DEFAULT_PROMPT_VERSION = "v1_fallback"
    settings.DEFAULT_CHAT_PIPELINE_TAG = "stable"

    # Expect a yaml.YAMLError when initializing the service
    with pytest.raises(yaml.YAMLError):
        PromptService(settings)


# Tests for get_prompt_version
def test_get_prompt_version_with_override_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Override tag 'experimental' exists and has 'chat' -> 'system' -> 'v2'
    version = service.get_prompt_version("chat", "system", "experimental")
    assert version == "v2"


def test_get_prompt_version_with_override_tag_not_in_config(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Override tag 'non_existent' does not exist, should fallback
    version = service.get_prompt_version("chat", "system", "non_existent")
    assert version == settings.DEFAULT_PROMPT_VERSION


def test_get_prompt_version_with_default_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # No override tag, default chat tag 'stable' exists and has 'chat' -> 'main_chat' -> 'v1'
    version = service.get_prompt_version("chat", "main_chat", None)
    assert version == "v1"


def test_get_prompt_version_with_default_tag_not_in_config(mock_settings):
    settings = MagicMock(spec=Settings)
    # Mock settings with a default tag that is NOT in the dummy config
    settings.PIPELINE_TAGS_CONFIG_PATH = str(
        mock_settings[2] / "config" / "pipeline-tags.yaml"
    )
    settings.DEFAULT_PROMPT_VERSION = "v1_fallback"
    settings.DEFAULT_CHAT_PIPELINE_TAG = "non_existent_default"

    service = PromptService(settings)

    # No override tag, default chat tag 'non_existent_default' not in config, should fallback
    version = service.get_prompt_version("chat", "system", None)
    assert version == settings.DEFAULT_PROMPT_VERSION


def test_get_prompt_version_with_pipeline_type_no_default_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Pipeline type 'other' has no default tag defined in mock settings, should fallback
    version = service.get_prompt_version("other", "some_prompt", None)
    assert version == settings.DEFAULT_PROMPT_VERSION


def test_get_prompt_version_prompt_name_not_in_config_for_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Override tag 'stable' exists, but 'chat' -> 'non_existent_prompt' is not defined, should fallback
    version = service.get_prompt_version("chat", "non_existent_prompt", "stable")
    assert version == settings.DEFAULT_PROMPT_VERSION


# Tests for get_prompt_content
@pytest.mark.asyncio  # Mark async tests
async def test_get_prompt_content_with_override_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Override tag 'experimental' exists and has 'chat' -> 'system' -> 'v2'
    # Expect content from app/features/chat/prompts/system/v2.j2
    content = await service.get_prompt_content("chat", "system", "experimental")
    assert content == "System prompt v2 content"


@pytest.mark.asyncio
async def test_get_prompt_content_with_default_tag(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # No override tag, default chat tag 'stable' exists and has 'chat' -> 'main_chat' -> 'v1'
    # Expect content from app/features/chat/prompts/main_chat/v1.j2
    content = await service.get_prompt_content("chat", "main_chat", None)
    assert content == "Main chat prompt v1 content"


@pytest.mark.asyncio
async def test_get_prompt_content_with_fallback(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Override tag 'non_existent' does not exist, should fallback to default version 'v1_fallback'
    # Expect content from app/features/chat/prompts/fallback_prompt/v1_fallback.j2
    # Note: This test assumes a fallback prompt file exists at the expected fallback path
    # based on the get_prompt_version logic and the dummy file structure.
    content = await service.get_prompt_content(
        "chat", "fallback_prompt", "non_existent"
    )
    assert content == "Fallback prompt content"


@pytest.mark.asyncio
async def test_get_prompt_content_file_not_found(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # Request a prompt that does not exist for the resolved version
    # This should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        await service.get_prompt_content("chat", "non_existent_prompt_file", "stable")


@pytest.mark.asyncio
async def test_get_prompt_content_cache(mock_settings):
    settings, _, _ = mock_settings
    service = PromptService(settings)

    # First call should read from file
    content1 = await service.get_prompt_content("chat", "system", "stable")
    assert content1 == "System prompt v1 content"
    assert len(service.prompt_content_cache_) == 1  # Cache should have one entry

    # Second call for the same prompt should use cache
    content2 = await service.get_prompt_content("chat", "system", "stable")
    assert content2 == "System prompt v1 content"
    assert len(service.prompt_content_cache_) == 1  # Cache size should not increase

    # Call for a different prompt should add to cache
    content3 = await service.get_prompt_content("chat", "main_chat", "stable")
    assert content3 == "Main chat prompt v1 content"
    assert len(service.prompt_content_cache_) == 2  # Cache should have two entries


# Tests for startup validation (from lifecycle.py)
# Note: These tests mock the PromptService to isolate the lifecycle logic.
# They also mock sys.exit to prevent the test runner from exiting.


@pytest.mark.asyncio
@patch("app.lifecycle.PromptService")  # Patch PromptService in the lifecycle module
@patch("sys.exit")  # Patch sys.exit
async def test_lifespan_successful_startup(
    mock_sys_exit, MockPromptService, mock_settings
):
    settings, _, _ = mock_settings

    # Configure the mocked PromptService instance
    mock_service_instance = AsyncMock()
    MockPromptService.return_value = mock_service_instance

    # Mock get_prompt_version to return a dummy version
    mock_service_instance.get_prompt_version.return_value = "mock_version"

    # Mock get_prompt_content to return dummy content and not raise errors
    mock_service_instance.get_prompt_content = AsyncMock(return_value="dummy content")

    # Mock the pipeline_tags_config_ attribute on the mocked instance
    mock_service_instance.pipeline_tags_config_ = {
        "some_tag": {}
    }  # Simulate config loaded

    # Create a dummy FastAPI app instance
    app = FastAPI()

    # Run the lifespan context manager
    async with lifespan(app):
        # If startup is successful, sys.exit should not be called
        mock_sys_exit.assert_not_called()

    # Ensure sys.exit was not called after exiting the lifespan context either
    mock_sys_exit.assert_not_called()


@pytest.mark.asyncio
@patch("app.lifecycle.PromptService")  # Patch PromptService in the lifecycle module
@patch("sys.exit")  # Patch sys.exit
async def test_lifespan_invalid_yaml_exits(
    mock_sys_exit, MockPromptService, mock_settings
):
    settings, _, _ = mock_settings

    # Configure the mocked PromptService instance to raise yaml.YAMLError on init
    MockPromptService.side_effect = yaml.YAMLError("Mock YAML Error")

    # Create a dummy FastAPI app instance
    app = FastAPI()

    # Run the lifespan context manager
    # We expect sys.exit to be called, so we don't expect the context manager to complete normally
    # The patch on sys.exit prevents the actual exit, allowing the test to continue
    async with lifespan(app):
        pass  # The lifespan context should not be fully entered in this failure case

    # Verify that sys.exit was called with a non-zero status code
    mock_sys_exit.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("app.lifecycle.PromptService")  # Patch PromptService in the lifecycle module
@patch("sys.exit")  # Patch sys.exit
async def test_lifespan_missing_prompt_file_exits(
    mock_sys_exit, MockPromptService, mock_settings
):
    settings, _, _ = mock_settings

    # Configure the mocked PromptService instance
    mock_service_instance = AsyncMock()
    MockPromptService.return_value = mock_service_instance

    # Mock get_prompt_version to return a dummy version
    mock_service_instance.get_prompt_version.return_value = "mock_version"

    # Configure get_prompt_content to raise FileNotFoundError for a specific prompt
    # We need to simulate the loop in lifecycle.py checking multiple prompts.
    # Let's make the first call succeed and the second fail.
    mock_service_instance.get_prompt_content.side_effect = [
        AsyncMock(return_value="dummy content")(),  # First call succeeds
        FileNotFoundError("Mock File Not Found Error"),  # Second call fails
    ]

    # Mock the pipeline_tags_config_ attribute on the mocked instance
    mock_service_instance.pipeline_tags_config_ = {
        "some_tag": {}
    }  # Simulate config loaded

    # Create a dummy FastAPI app instance
    app = FastAPI()

    # Run the lifespan context manager
    # We expect sys.exit to be called
    async with lifespan(app):
        pass  # The lifespan context should not be fully entered

    # Verify that sys.exit was called with a non-zero status code
    mock_sys_exit.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("app.lifecycle.PromptService")  # Patch PromptService in the lifecycle module
@patch("sys.exit")  # Patch sys.exit
async def test_lifespan_generic_exception_exits(
    mock_sys_exit, MockPromptService, mock_settings
):
    settings, _, _ = mock_settings

    # Configure the mocked PromptService instance to raise a generic Exception on init
    MockPromptService.side_effect = Exception("Mock Generic Exception")

    # Create a dummy FastAPI app instance
    app = FastAPI()

    # Run the lifespan context manager
    # We expect sys.exit to be called
    async with lifespan(app):
        pass  # The lifespan context should not be fully entered

    # Verify that sys.exit was called with a non-zero status code
    mock_sys_exit.assert_called_once_with(1)


# Add tests for other startup validation failure cases later
