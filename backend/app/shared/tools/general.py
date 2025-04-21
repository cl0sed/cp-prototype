import logging
import datetime
from typing import List

from haystack.tools import Tool

logger = logging.getLogger(__name__)


# Tool function for getting the current time
def get_current_time_tool_func(**kwargs):
    """
    Gets the current date and time.
    """
    logger.info("Executing get_current_time tool")
    return {"current_time": datetime.datetime.now().isoformat()}


# Tool definition for getting the current time
get_current_time_tool = Tool(
    name="get_current_time",
    description="Useful for getting the current date and time.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
    function=get_current_time_tool_func,
)


# List of all defined tools
general_tools: List[Tool] = [get_current_time_tool]
