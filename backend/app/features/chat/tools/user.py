import logging
import uuid
from typing import Dict, Any, List
from haystack.tools import Tool
from app.db.models.user import User  # Import User
from app.services.user_service import UserService  # Import UserService

logger = logging.getLogger(__name__)


# Tool function for getting user tasks
# This function will receive the 'state' object from the Agent's run method,
# which should contain the DB session and user object.
async def get_user_tasks_tool_func(state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Gets the tasks for the specified user.
    Requires 'user' object and 'user_service' in the state.
    Performs role check: only 'admin' can see all tasks, others see their own.
    """
    logger.info("Executing get_user_tasks tool")
    user: User = state.get("user")
    user_service: UserService = state.get("user_service")  # Get UserService from state
    # Extract user_id from kwargs if the tool call provides it, otherwise use the user from state
    # This allows the LLM to specify a user ID if needed, but defaults to the current user.
    target_user_id_str = kwargs.get("user_id")
    target_user_id = (
        uuid.UUID(target_user_id_str) if target_user_id_str else user.id
    )  # Assuming user.id is UUID
    if not user or not user_service:  # Check for user and user_service
        logger.error("get_user_tasks tool requires 'user' and 'user_service' in state.")
        return {"error": "Internal tool error: User or UserService not available."}
    # Role check: Only admin can request tasks for other users
    if target_user_id != user.id and user.role != "admin":
        logger.warning(
            f"User {user.id} (role: {user.role}) attempted to access tasks for user {target_user_id}"
        )
        return {"error": "You do not have permission to access tasks for other users."}
    try:
        # Use the UserService to fetch tasks
        tasks = await user_service.get_user_tasks(user_id=target_user_id)
        logger.info(f"Found {len(tasks)} tasks for user {target_user_id}")
        return {"tasks": tasks}
    except Exception as e:
        logger.error(
            f"Error fetching tasks for user {target_user_id}: {e}", exc_info=True
        )
        return {"error": f"Failed to retrieve tasks: {e}"}


# Tool definition for getting user tasks
get_user_tasks_tool = Tool(
    name="get_user_tasks",
    description="Useful for getting the list of tasks assigned to a user. Requires user_id.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The ID of the user whose tasks are requested (defaults to the current user if not specified).",
            }
        },
        "required": [],  # user_id is optional in the tool call, defaults to current user
        "additionalProperties": False,
    },
    function=get_user_tasks_tool_func,
)
# List of chat-specific tools
chat_tools: List[Tool] = [get_user_tasks_tool]
