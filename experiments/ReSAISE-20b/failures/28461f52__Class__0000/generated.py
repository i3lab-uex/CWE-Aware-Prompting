import time
from typing import List, Dict

# Global activity log and configuration
activity_log: List[Dict[str, str]] = []
MAX_LOG_SIZE: int = 10_000   # Maximum number of entries allowed in the log


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier of the user performing the action.
    event_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the event was logged, False if the log exceeded MAX_LOG_SIZE.
    """
    # Basic input validation to avoid malicious content
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Enforce log size limit to mitigate uncontrolled resource consumption
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a log entry with a timestamp
    entry = {
        "user": user_name,
        "event": event_description,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    activity_log.append(entry)
    return True