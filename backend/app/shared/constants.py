"""
Shared Constants and Enumerations.

This file contains constant values and enumerations (Enums) that are used
across multiple features or modules within the backend application.

Examples:
- Status codes or states (e.g., TaskStatus.PENDING, TaskStatus.COMPLETED).
- Predefined string literals or numerical values with specific meanings.
- Configuration keys if used consistently across modules.

Keep this for truly shared, static values. Avoid putting configuration settings
(which should be in config.py) or feature-specific constants here.
"""

from saq.job import Status  # noqa

# Re-export SAQ's Status enum for direct use throughout the application
# Status includes: NEW, QUEUED, ACTIVE, COMPLETE, ABORTING, ABORTED, FAILED

# Also re-export SAQ's status groupings
from saq.job import (  # noqa
    ACTIVE_STATUSES,  # {Status.NEW, Status.QUEUED, Status.ACTIVE}
    TERMINAL_STATUSES,  # {Status.COMPLETE, Status.FAILED, Status.ABORTED}
    UNSUCCESSFUL_TERMINAL_STATUSES,  # TERMINAL_STATUSES - {Status.COMPLETE}
)


# Add application-specific statuses if needed
class AppJobStatus:
    """Additional application-specific job status constants"""

    PENDING_RETRY = "pending_retry"
