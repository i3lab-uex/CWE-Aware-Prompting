import datetime
from typing import List, Dict

# Global activity log list
activity_log: List[Dict[str, str]] = []

# Maximum number of entries the log can hold
MAX_LOG_SIZE: int = 100_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the event was successfully logged, False if the log is at capacity.
    """
    # Reject logging if we have reached the maximum size
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Construct the log entry
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_key": user_key,
        "action_details": action_details,
    }

    # Append to the global log
    activity_log.append(entry)
    return True