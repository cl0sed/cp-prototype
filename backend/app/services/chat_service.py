import logging
import uuid
from typing import List, Dict, Any, Optional, cast
from haystack.dataclasses import (
    ChatMessage as HaystackChatMessage,
    ChatRole,
)  # Import Haystack ChatMessage and ChatRole
from haystack.components.generators.chat import (
    OpenAIChatGenerator,
)  # Import the generator
from haystack.utils import Secret  # Import Secret for LLM API key

from app.services.user_service import (
    UserService,
    get_user_service,
)  # Import UserService and its dependency function

from fastapi import HTTPException, status, Depends  # Import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import Settings, get_settings
from app.db.models.chat import ChatMessage  # Import ChatMessage
from app.db import models  # Import the models module to avoid circular dependency
from app.features.chat.chat_pipeline import (
    build_chat_pipeline,
)  # Import the new pipeline builder
from app.services.prompt_service import (
    PromptService,
    get_prompt_service,
)  # Import PromptService and its dependency function
from app.shared.exceptions import PromptTemplateNotFoundError  # Import custom exception

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service for handling chat interactions with the AI agent.
    Orchestrates the Haystack pipeline.
    """

    def __init__(
        self,
        settings: Settings,
        prompt_service: PromptService,
        user_service: UserService,
    ):
        """
        Initializes the ChatService.

        Args:
            settings: Application settings.
            prompt_service: The PromptService instance.
            user_service: The UserService instance.
        """
        self.settings = settings
        self.prompt_service = prompt_service
        self.user_service = user_service  # Store UserService instance
        pass  # Pipeline will be built in interact method via dependency

    async def generate_greeting(self, db: AsyncSession, user_id: uuid.UUID) -> str:
        """
        Generates a dynamic greeting for the user based on past interactions.
        """
        logger.info(f"Generating dynamic greeting for user {user_id}.")

        try:
            # Fetch User object to get username
            # from app.db.models.user import User  # Local import to break circular dependency
            user = await db.get(models.User, user_id)
            logger.debug(
                f"DEBUG: User fetched in generate_greeting: {user}, type: {type(user)}"
            )
            if not user:
                logger.error(
                    f"ERROR: User not found in DB for ST ID {user_id} in generate_greeting"
                )
                # Depending on how this is called, might raise HTTPException or a custom error
                # For now, raise a generic Exception which the caller should handle
                raise Exception("User not found")

            # Fetch recent chat history for the user (e.g., last 10 messages across sessions)
            # This is a simplified approach; a more sophisticated method might summarize history.
            history_result = await db.execute(
                select(ChatMessage)
                .filter(ChatMessage.user_id == user_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(10)  # Limit to the last 10 messages for context
            )
            chat_history_models = list(history_result.scalars().all())
            chat_history_models.reverse()  # Reverse to chronological order

            # Format history for the prompt
            history_text = "\n".join(
                [
                    f"{msg.role.capitalize()}: {msg.content}"
                    for msg in chat_history_models
                ]
            )

            # Fetch greeting prompt template using the injected service
            logger.debug("DEBUG: Calling get_prompt_content for greeting prompt")
            greeting_prompt_template = (
                await self.prompt_service.get_prompt_template_content(
                    pipeline_type="chat",  # Specify pipeline type
                    logical_prompt_name="greeting",  # Specify logical prompt name
                    override_pipeline_tag=None,  # Use default tag for API calls
                )
            )
            logger.debug("DEBUG: Greeting prompt template fetched successfully")

            # Instantiate LLM Generator - Initialize here as it's specific to this task
            llm_generator = OpenAIChatGenerator(
                api_key=Secret.from_token(self.settings.LLM_API_KEY.get_secret_value()),
                model=self.settings.LLM_MODEL,
                # api_base_url=self.settings.LLM_API_URL if self.settings.LLM_API_URL else None,
            )

            # Format the prompt with user details and history
            # Assuming the greeting prompt template expects 'username' and 'history'
            formatted_prompt = greeting_prompt_template.format(
                username=user.username if user.username else "there",
                history=history_text,
            )
            logger.debug(
                f"DEBUG: Formatted greeting prompt: {formatted_prompt[:200]}..."
            )  # Log start of prompt

            # Call the LLM to generate the greeting
            # The generator expects a list of Haystack ChatMessage objects
            # For a simple prompt, we can create a single user message
            messages_for_llm = [
                HaystackChatMessage.from_user(formatted_prompt)
            ]  # Use Haystack ChatMessage

            logger.debug("DEBUG: Calling LLM generator for greeting")
            result = await llm_generator.run(messages=messages_for_llm)
            logger.debug(f"DEBUG: LLM generator result: {result}")

            # Extract the greeting text from the LLM response
            # Assuming the generator returns a list of messages in 'replies'
            greeting_text = ""
            if result and result.get("replies"):
                # Find the first assistant message
                for reply in result["replies"]:
                    # Need to import ChatRole if not already imported
                    if reply.role == ChatRole.ASSISTANT and reply.content:
                        greeting_text = reply.content
                        break  # Take the first assistant reply

            if not greeting_text:
                logger.warning("LLM generator did not return a valid greeting.")
                # Fallback to a simple greeting if LLM fails
                greeting_text = f"Hello, {user.username if user.username else 'there'}!"

            logger.debug(f"DEBUG: Generated greeting text: {greeting_text}")
            return greeting_text

        except Exception as e:
            logger.error(
                f"ERROR: Exception during greeting generation for user {user_id}: {e}",
                exc_info=True,
            )
            # Re-raise the exception for the caller (router) to handle
            raise e

    async def interact(
        self,
        db: AsyncSession,
        user_message: str,
        user: models.User,  # Use models.User for type hinting
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Processes a user message and conversation history to generate an agent response.

        Args:
            db: The SQLAlchemy async database session.
            user_message: The current message from the user.
            user: The authenticated user object.
            session_id: Optional ID of the current chat session. If None, a new session is created.

        Returns:
            A dictionary containing the agent's reply and the session ID.
        """
        try:
            logger.info(
                f"Processing chat interaction for user {user.id} in session {session_id}"
            )

            # Determine the current session ID
            current_session_id = session_id if session_id else str(uuid.uuid4())

            # Store the user's message in the database
            user_chat_message = ChatMessage(
                user_id=user.id,
                session_id=current_session_id,
                role="user",
                content=user_message,
            )
            db.add(user_chat_message)
            await db.commit()
            await db.refresh(
                user_chat_message
            )  # Refresh to get the generated ID and timestamp

            # Fetch recent chat history for this session from the database
            # Use the index on (session_id, timestamp) for efficient retrieval
            # history_result = await db.execute(
            #     select(ChatMessage)
            #     .filter(ChatMessage.session_id == current_session_id)
            #     .order_by(ChatMessage.timestamp)
            # )
            # chat_history_models = history_result.scalars().all()

            # Convert database models to Haystack ChatMessage objects
            # Include the current user message in the history for the pipeline
            # messages: List[ChatMessage] = []
            # for msg in chat_history_models:
            #     # Map DB role to Haystack ChatRole enum
            #     haystack_role = (
            #         ChatRole.USER
            #         if msg.role == "user"
            #         else (
            #             ChatRole.ASSISTANT if msg.role == "assistant" else ChatRole.TOOL
            #         )
            #     )
            #     meta_data = {
            #         "db_id": str(msg.id),
            #         "timestamp": msg.timestamp.isoformat(),
            #         **(msg.metadata_ or {}),
            #     }
            #     if haystack_role == ChatRole.USER:
            #         messages.append(
            #             HaystackChatMessage.from_user(msg.content, meta=meta_data)
            #         )
            #     elif haystack_role == ChatRole.ASSISTANT:
            #         messages.append(
            #             HaystackChatMessage.from_assistant(msg.content, meta=meta_data)
            #         )
            #     elif haystack_role == ChatRole.TOOL:
            #         messages.append(
            #             HaystackChatMessage.from_tool(msg.content, meta=meta_data)
            #         )
            #     # Add other roles if necessary, though the DB schema currently only supports user/assistant/tool
            #     else:
            #         logger.warning(
            #             f"Unknown chat message role from DB: {msg.role}. Skipping message."
            #         )

            pipeline = await build_chat_pipeline(
                pipeline_type="chat",  # Specify the pipeline type
                override_pipeline_tag=None,  # Use default tag for ChatService interactions
                prompt_service=self.prompt_service,
                settings_obj=self.settings,  # Pass settings as it's needed by the generator (using settings_obj as per pipeline signature)
                # db=db # Pass db if needed by any pipeline components
            )

            pipeline_result = await pipeline.run_async(
                data={
                    "agent": {  # Target the 'agent' component in the pipeline
                        "messages": [
                            HaystackChatMessage.from_user(user_message)
                        ],  # Pass only the current user message
                        "user": user,  # Pass the user object for tool checks
                        "session_id": current_session_id,  # Pass the session ID
                        # Add other context data needed by tools or prompts here
                    }
                }
            )

            # Process the pipeline result
            # The Agent returns the full conversation history including its responses
            replies: List[ChatMessage] = pipeline_result["agent"]["messages"]

            # Store agent and tool messages in the database
            messages_to_save = []
            final_reply_text = ""
            for reply_msg in replies:
                logger.debug(
                    f"Processing reply message with role: {reply_msg.role}, meta: {reply_msg.meta}"
                )  # Log meta content
                # Only save messages generated by the assistant or tools
                if reply_msg.role in [ChatRole.ASSISTANT, ChatRole.TOOL]:
                    messages_to_save.append(
                        ChatMessage(
                            user_id=user.id,
                            session_id=current_session_id,
                            role=reply_msg.role.value,  # Save the enum value (string)
                            content=reply_msg.text,  # Save the content from the Haystack message
                            metadata_=reply_msg.meta,  # Save metadata (e.g., tool call details, usage)
                        )
                    )
                if reply_msg.role == ChatRole.ASSISTANT and reply_msg.text is not None:
                    final_reply_text = (
                        reply_msg.text
                    )  # Capture the last assistant text reply

            if messages_to_save:
                db.add_all(messages_to_save)
                await db.commit()
                # No need to refresh here unless we need the IDs immediately

            logger.info(
                f"Finished processing chat interaction for user {user.id} in session {current_session_id}"
            )

            # Return the agent's final text reply and the session ID
            return {"reply": final_reply_text, "session_id": current_session_id}

        except PromptTemplateNotFoundError as e:
            logger.error(f"Prompt template not found: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Required prompt template not found: {e}",
            ) from e

        except Exception as e:
            logger.error(
                f"An unexpected error occurred in ChatService: {e}", exc_info=True
            )
            # Re-raise as HTTPException or handle as appropriate for the service layer
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred during chat processing.",
            ) from e

    async def get_history(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        session_id: Optional[str] = None,
        limit: int = 5,
    ) -> List[ChatMessage]:
        """
        Retrieves chat message history for the given user.
        Can filter by session_id or retrieve recent messages across sessions.

        Args:
            db: The SQLAlchemy async database session.
            user_id: The ID of the user.
            session_id: Optional ID of the chat session to filter by.
            limit: The maximum number of messages to retrieve.

        Returns:
            A list of ChatMessage ORM models.
        """
        logger.info(
            f"Fetching chat history for user {user_id}, session_id: {session_id}, limit: {limit}"
        )

        try:
            query = select(ChatMessage).filter(
                ChatMessage.user_id == user_id
            )  # Use user_id directly

            if session_id:
                # Filter by session_id and order by timestamp (uses ix_chat_message_session_timestamp)
                query = query.filter(
                    ChatMessage.session_id == str(session_id)
                ).order_by(ChatMessage.timestamp)
            else:
                # Order by timestamp descending to get recent messages across sessions (uses ix_chat_message_user_timestamp)
                query = query.order_by(ChatMessage.timestamp.desc())

            query = query.limit(limit)

            result = await db.execute(query)
            messages = list(result.scalars().all())

            # If fetching recent across sessions, reverse to show in chronological order
            if not session_id:
                messages.reverse()

            logger.info(f"Found {len(messages)} chat messages for user {user_id}")
            return cast(List[ChatMessage], messages)

        except Exception as e:
            logger.error(
                f"Failed to fetch chat history for user {user_id}: {e}", exc_info=True
            )
            # Re-raise the exception for the caller (router) to handle
            raise e


# Dependency to get ChatService instance (will be used in the router)
async def get_chat_service(
    settings: Settings = Depends(get_settings),
    prompt_service: PromptService = Depends(get_prompt_service),
    user_service: UserService = Depends(get_user_service),
) -> ChatService:
    """
    FastAPI dependency to provide a ChatService instance.
    """
    logger.debug("DEBUG: Entering get_chat_service dependency function")

    chat_service = ChatService(
        settings=settings, prompt_service=prompt_service, user_service=user_service
    )
    logger.debug("DEBUG: get_chat_service dependency called and returning instance")
    return chat_service
