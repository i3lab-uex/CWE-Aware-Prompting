# activity_logger.py

from datetime import datetime
from typing import List, Tuple

# Global list that stores activity records.
# Each record is a tuple: (timestamp, user_identifier, event)
activity_log: List[Tuple[str, str, str]] = []

# Maximum number of entries allowed in the activity log.
MAX_LOG_SIZE: int = 10_000


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was added successfully, False if the log has reached its size limit.
    """
    # Prevent uncontrolled growth by enforcing a maximum size
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Use ISO format for timestamp to avoid timezone ambiguities
    timestamp = datetime.utcnow().isoformat() + "Z"
    activity_log.append((timestamp, user_identifier, event))
    return True