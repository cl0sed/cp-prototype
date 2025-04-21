import logging
from typing import Dict, Optional  # Import Optional
from fastapi import Depends
from app.config import Settings, get_settings
from app.shared.exceptions import (
    PromptTemplateNotFoundError,
)  # Import custom exception from shared

# Import necessary modules for file handling
import os
from pathlib import Path
import yaml  # Import yaml for config file parsing

logger = logging.getLogger(__name__)


class PromptService:
    """
    Service for managing and retrieving prompt templates from the file system
    based on pipeline tags and configuration, with a configurable fallback version.
    """

    def __init__(self, settings: Settings):
        """
        Initializes the PromptService by loading the pipeline tags configuration.

        Args:
            settings: Application settings containing prompt configuration paths and defaults.
        """
        self.settings = settings
        self.default_prompt_version = settings.DEFAULT_PROMPT_VERSION
        self.pipeline_tags_config_: Dict[
            str, Dict[str, Dict[str, str]]
        ] = {}  # Stores the parsed pipeline-tags.yaml
        self.prompt_content_cache_: Dict[
            str, str
        ] = {}  # Cache for prompt file content (key: file_path)

        logger.debug("DEBUG: Entering PromptService constructor")

        # Load the pipeline tags override configuration file
        config_path = settings.PIPELINE_TAGS_CONFIG_PATH
        try:
            full_config_path = Path(config_path)  # Assume path is relative to CWD

            if not full_config_path.is_file():
                logger.warning(
                    f"Pipeline tags configuration file not found at {config_path}. Using empty configuration."
                )
                self.pipeline_tags_config_ = {}
            else:
                with open(full_config_path, "r", encoding="utf-8") as f:
                    self.pipeline_tags_config_ = (
                        yaml.safe_load(f) or {}
                    )  # Use empty dict if file is empty
                logger.info(
                    f"Successfully loaded pipeline tags configuration from {config_path}"
                )
                logger.debug(
                    f"Loaded config keys: {list(self.pipeline_tags_config_.keys())}"
                )

        except yaml.YAMLError as e:
            logger.error(
                f"Failed to parse pipeline tags configuration file at {config_path}: {e}"
            )
            # Re-raise the YAML error to be caught by startup validation
            raise e
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while loading pipeline tags configuration from {config_path}: {e}",
                exc_info=True,
            )
            self.pipeline_tags_config_ = {}

        logger.debug("DEBUG: PromptService initialized.")

    def get_prompt_template_version(
        self,
        pipeline_type: str,
        logical_prompt_name: str,
        override_pipeline_tag: Optional[str],
    ) -> str:
        """
        Determines the target prompt version based on override tag, default tag,
        and the loaded pipeline tags configuration, falling back to the default version.

        Args:
            pipeline_type: The type of pipeline (e.g., 'chat', 'creatordna').
            logical_prompt_name: The logical name of the prompt (e.g., 'system', 'greeting').
            override_pipeline_tag: An optional tag to override the default pipeline tag.

        Returns:
            The resolved prompt version string.
        """
        tag_to_use = override_pipeline_tag

        # If no override tag, determine the default tag based on pipeline_type
        if tag_to_use is None:
            # This logic maps pipeline_type to the correct default tag setting from config.py
            # Add more pipeline types here as needed
            if pipeline_type == "chat":
                tag_to_use = self.settings.DEFAULT_CHAT_PIPELINE_TAG
            # elif pipeline_type == "creatordna":
            #     tag_to_use = self.settings.DEFAULT_CREATORDNA_PIPELINE_TAG
            else:
                # Fallback to default prompt version if pipeline_type doesn't have a defined default tag
                logger.warning(
                    f"No default pipeline tag defined for pipeline type '{pipeline_type}'. Using default prompt version '{self.default_prompt_version}'."
                )
                return self.default_prompt_version

        # Look up the version in the loaded configuration
        tag_config = self.pipeline_tags_config_.get(tag_to_use, {})
        type_config = tag_config.get(pipeline_type, {})
        version = type_config.get(logical_prompt_name)

        if version:
            logger.debug(
                f"Resolved version '{version}' for prompt '{logical_prompt_name}' under tag '{tag_to_use}' and type '{pipeline_type}'."
            )
            return version
        else:
            logger.debug(
                f"No specific version found for prompt '{logical_prompt_name}' under tag '{tag_to_use}' and type '{pipeline_type}'. Using default prompt version '{self.default_prompt_version}'."
            )
            return self.default_prompt_version

    async def get_prompt_template_content(
        self,
        pipeline_type: str,
        logical_prompt_name: str,
        override_pipeline_tag: Optional[str] = None,
    ) -> str:
        """
        Retrieves the content of a prompt template from the file system.

        Args:
            pipeline_type: The type of pipeline (e.g., 'chat', 'creatordna').
            logical_prompt_name: The logical name of the prompt (e.g., 'system', 'greeting').
            override_pipeline_tag: An optional tag to override the default pipeline tag.

        Returns:
            The content of the prompt template.

        Raises:
            FileNotFoundError: If the prompt file does not exist.
            PromptTemplateNotFoundError: If the prompt version cannot be resolved or file reading fails.
        """
        try:
            target_version = self.get_prompt_template_version(
                pipeline_type, logical_prompt_name, override_pipeline_tag
            )

            # Determine scope (feature or shared) and construct file path
            # This logic maps pipeline_type to the correct scope directory
            # Add more pipeline types and their scopes here as needed
            if pipeline_type == "chat":
                scope = "features/chat"
            # elif pipeline_type == "creatordna":
            #     scope = "features/creatordna" # Example
            else:
                # Default to shared for other types, adjust as needed
                scope = "shared"
                logger.warning(
                    f"Assuming shared scope for pipeline type '{pipeline_type}'. Adjust PromptService.get_prompt_template_content if needed."
                )

            # Construct the file path relative to the container's WORKDIR (/app)
            # Files are copied to /app/app/... inside the container
            file_path_relative = (
                Path("app")
                / scope
                / "prompts"
                / logical_prompt_name
                / f"{target_version}.j2"
            )

            # Check cache first
            if file_path_relative in self.prompt_content_cache_:
                logger.debug(
                    f"Returning cached content for prompt file: {file_path_relative}"
                )
                return self.prompt_content_cache_[str(file_path_relative)]

            # Read the file content
            # Use pathlib for robust path handling
            full_file_path = Path(os.getcwd()) / file_path_relative

            if not full_file_path.is_file():
                logger.error(f"Prompt file not found: {full_file_path}")
                raise FileNotFoundError(f"Prompt file not found: {file_path_relative}")

            with open(full_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Cache the content
            self.prompt_content_cache_[str(file_path_relative)] = content
            logger.debug(
                f"Successfully loaded and cached prompt file: {file_path_relative}"
            )

            return content

        except FileNotFoundError:
            # Re-raise FileNotFoundError as it's a specific expected error
            raise
        except Exception as e:
            logger.error(
                f"Failed to get prompt content for '{logical_prompt_name}' (type: {pipeline_type}, tag: {override_pipeline_tag}): {e}",
                exc_info=True,
            )
            # Wrap other exceptions in PromptTemplateNotFoundError for consistency
            raise PromptTemplateNotFoundError(
                f"Failed to get prompt content for '{logical_prompt_name}': {e}"
            ) from e


async def get_prompt_service(
    settings: Settings = Depends(get_settings),
) -> PromptService:
    """
    FastAPI dependency to provide a PromptService instance.
    """

    prompt_service = PromptService(settings)

    return prompt_service
