import logging
import yaml
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI  # Import FastAPI for type hinting
from app.config import get_settings  # Import get_settings
from app.services.prompt_service import PromptService  # Import PromptService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    Includes configuration validation and prompt file checks.
    """
    logger.info("Application startup initiated.")

    # 1. Load Settings and log config paths/defaults (Pydantic handles ENV VAR loading)
    settings_obj = get_settings()  # Get the settings instance
    logger.info(
        f"Configured PIPELINE_TAGS_CONFIG_PATH: {settings_obj.PIPELINE_TAGS_CONFIG_PATH}"
    )
    logger.info(
        f"Configured DEFAULT_PROMPT_VERSION: {settings_obj.DEFAULT_PROMPT_VERSION}"
    )
    logger.info(
        f"Configured DEFAULT_CHAT_PIPELINE_TAG: {settings_obj.DEFAULT_CHAT_PIPELINE_TAG}"
    )

    # 2. Attempt to load and parse the override YAML file via PromptService
    try:
        # Instantiating PromptService here triggers the config loading/parsing
        # It will raise yaml.YAMLError if the file is invalid
        prompt_service_instance = PromptService(settings_obj)  # Use the settings object
        logger.info(
            "Pipeline tags configuration file loaded and parsed successfully (if present)."
        )

    except FileNotFoundError:
        # This case is handled with a WARNING in PromptService, no need to exit here.
        logger.warning(
            f"Pipeline tags configuration file not found at {settings_obj.PIPELINE_TAGS_CONFIG_PATH}. Proceeding with default configuration."
        )
        # Create a PromptService instance with empty config if file not found
        prompt_service_instance = PromptService(
            settings_obj
        )  # Re-instantiate to ensure it has the empty config

    except yaml.YAMLError as e:
        logger.error(
            f"Invalid pipeline tags configuration file at {settings_obj.PIPELINE_TAGS_CONFIG_PATH}: {e}"
        )
        logger.error("Application startup failed due to invalid configuration file.")
        sys.exit(1)  # Exit the application on invalid YAML
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during configuration loading: {e}",
            exc_info=True,
        )
        logger.error("Application startup failed due to configuration error.")
        sys.exit(1)  # Exit on other unexpected errors during config loading

    # 3. Check Prompt Files for Default Tags
    default_tags = {
        "chat": settings_obj.DEFAULT_CHAT_PIPELINE_TAG,
        # Add other default tags here as needed
        # "creatordna": settings.DEFAULT_CREATORDNA_PIPELINE_TAG,
    }
    expected_prompts = {
        "chat": ["system", "greeting", "main_chat"],
        # Define expected prompts for other pipeline types here
        # "creatordna": ["system", "analysis_prompt", "report_prompt"],
    }

    missing_files = []
    effective_config_summary = {
        "default_tags": default_tags,
        "resolved_prompt_versions": {},
    }

    for pipeline_type, default_tag in default_tags.items():
        effective_config_summary["resolved_prompt_versions"][pipeline_type] = {}
        prompts_for_type = expected_prompts.get(pipeline_type, [])

        for prompt_name in prompts_for_type:
            try:
                # Use PromptService.get_prompt_content to check if the file is accessible
                # This method handles version resolution and file reading/existence check
                await prompt_service_instance.get_prompt_template_content(
                    pipeline_type=pipeline_type,
                    logical_prompt_name=prompt_name,
                    override_pipeline_tag=None,  # Check for the default tag
                )
                # If successful, log the resolved version for the summary
                target_version = prompt_service_instance.get_prompt_template_version(
                    pipeline_type=pipeline_type,
                    logical_prompt_name=prompt_name,
                    override_pipeline_tag=None,  # Check for the default tag
                )
                effective_config_summary["resolved_prompt_versions"][pipeline_type][
                    prompt_name
                ] = target_version

            except FileNotFoundError:
                # Catch FileNotFoundError specifically raised by PromptService
                # Construct the expected path for the error message based on PromptService logic
                target_version = prompt_service_instance.get_prompt_template_version(
                    pipeline_type=pipeline_type,
                    logical_prompt_name=prompt_name,
                    override_pipeline_tag=None,
                )
                scope = (
                    "features/chat" if pipeline_type == "chat" else "shared"
                )  # Replicate scope logic
                expected_path_relative = (
                    f"backend/app/{scope}/prompts/{prompt_name}/{target_version}.j2"
                )
                missing_files.append(expected_path_relative)
                logger.error(
                    f"Required prompt file not found for default configuration: {expected_path_relative}"
                )

            except Exception as e:
                # Catch any other exceptions during prompt fetching
                logger.error(
                    f"Error fetching prompt content for '{prompt_name}' (type: {pipeline_type}, tag: {default_tag}): {e}",
                    exc_info=True,
                )
                missing_files.append(
                    f"{pipeline_type}/{prompt_name} (Error fetching content)"
                )

    if missing_files:
        logger.error(
            "Application startup failed due to missing required prompt files for default configuration:"
        )
        for missing in missing_files:
            logger.error(f"- {missing}")
        sys.exit(1)  # Exit the application if required files are missing

    # 4. Log Effective Config
    logger.info("Effective Prompt Configuration Summary:")
    logger.info(
        f"  Override file loaded: {bool(prompt_service_instance.pipeline_tags_config_)}"
    )
    logger.info(
        f"  Default Prompt Version (Fallback): {settings_obj.DEFAULT_PROMPT_VERSION}"
    )
    logger.info("  Resolved Versions for Default Pipeline Tags:")
    for p_type, prompts in effective_config_summary["resolved_prompt_versions"].items():
        logger.info(f"    {p_type}:")
        for p_name, version in prompts.items():
            logger.info(f"      {p_name}: {version}")

    logger.info("Application startup complete.")
    yield  # Application runs
    logger.info("Application shutdown initiated.")
