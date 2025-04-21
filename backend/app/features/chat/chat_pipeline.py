from haystack.core.pipeline import AsyncPipeline  # Import AsyncPipeline
from haystack.components.agents import Agent  # Import the Agent component
from haystack.utils import Secret  # Import Haystack's Secret class

# Import the User model for state schema type hinting
from app.db.models.user import User  # Import User model

# Import shared tools
from app.shared.tools.general import general_tools  # Import the list of general tools

# Import a standard Haystack generator
from haystack.components.generators.chat import OpenAIChatGenerator

# Import settings to get Portkey keys and URL
from app.config import Settings  # Import get_settings


# Define the chat pipeline
from app.services.prompt_service import PromptService  # Import PromptService
from typing import Optional  # Import Optional


# Define the chat pipeline
async def build_chat_pipeline(  # Make async as it will call async get_prompt_template_content
    *,  # Enforce keyword-only arguments after this
    pipeline_type: str,
    override_pipeline_tag: Optional[str],
    prompt_service: PromptService,
    # Add other dependencies needed by components here (e.g., settings, db)
    settings: Settings,  # Assuming settings is needed by generator, explicitly type-hint as Settings
    # db # Assuming db might be needed by future components, though not by PromptService now
) -> AsyncPipeline:  # Update return type hint
    """
    Builds the minimal chat Haystack pipeline using OpenAIChatGenerator.

    Returns:
        A configured Haystack Pipeline.
    """
    pipeline = AsyncPipeline()  # Instantiate AsyncPipeline

    # Configure OpenAIChatGenerator to use Portkey
    # Use the Portkey Virtual Key as the API key
    # Use the Portkey API base URL
    # Specify the desired model name (Portkey will route this)
    # Instantiate a standard LLM Generator (replace with the actual desired generator)
    # Assuming OpenAIChatGenerator for now, using settings for API key and model
    llm_generator = OpenAIChatGenerator(
        api_key=Secret.from_token(
            settings.LLM_API_KEY.get_secret_value()
        ),  # Create a Haystack Secret from the Pydantic SecretStr value
        model=settings.LLM_MODEL,  # Use the configurable LLM model from settings
        # Add other parameters as needed by the chosen generator
        api_base_url=str(settings.LLM_API_URL)
        if settings.LLM_API_URL
        else None,  # Use configurable API URL if applicable
    )

    # Fetch prompts using the PromptService
    # Note: This assumes 'system' and 'main_chat' are the logical prompt names needed.
    # Adjust if the pipeline requires other prompts.
    system_prompt_content = await prompt_service.get_prompt_template_content(
        pipeline_type=pipeline_type,
        logical_prompt_name="system",
        override_pipeline_tag=override_pipeline_tag,
    )
    # main_chat_prompt_content = await prompt_service.get_prompt_template_content(
    #     pipeline_type=pipeline_type,
    #     logical_prompt_name="main_chat",
    #     override_pipeline_tag=override_pipeline_tag,
    # )

    # Instantiate the Haystack Agent
    # The Agent will use the llm_generator and the system prompt
    # The main_chat prompt template will be used by the Agent's internal PromptBuilder
    # We don't explicitly add a separate PromptBuilder component here unless customizing the Agent's behavior.
    # If the Agent needs the main_chat_prompt_content passed explicitly, this would be done here
    # or in the run_async call depending on the Agent's API.
    # For now, assume the Agent uses the system_prompt and the messages passed in run_async.
    # Tools will be added later when implementing function calling.
    agent = Agent(
        chat_generator=llm_generator,  # Corrected keyword argument from 'llm' to 'chat_generator'
        system_prompt=system_prompt_content,
        # The Agent component in Haystack 2.0 handles conversation history and tool calling internally.
        # The main_chat_prompt template will be used by the Agent's internal PromptBuilder
        # We don't explicitly add a separate PromptBuilder component here unless customizing the Agent's behavior.
        # If the Agent needs the main_chat_prompt_content passed explicitly, this would be done here
        # or in the run_async call depending on the Agent's API.
        # For now, assume the Agent uses the system_prompt and the messages passed in run_async.
        # Tools will be added later when implementing function calling.
        tools=list(
            general_tools
        ),  # Provide the list of general tools to the Agent, explicitly creating a new list
        state_schema={  # Define the schema for additional inputs
            "user": {"type": User},  # Expect a User object
            "session_id": {"type": str},  # Expect a string session ID
        },
    )

    # Add components
    # Add the Agent to the pipeline
    pipeline.add_component("agent", agent)

    # No explicit connections are needed for the Agent in this minimal setup.
    # The Agent component handles the flow from input messages to LLM and back.

    return pipeline
