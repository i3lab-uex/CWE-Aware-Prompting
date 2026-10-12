import threading
from typing import List

# Global activity log and its configuration
MAX_LOG_SIZE: int = 10_000          # maximum number of entries allowed in the log
activity_log: List[dict] = []       # list that stores activity records

# Lock to protect concurrent access to the log
_log_lock = threading.Lock()


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Records a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user who performed the action.
    event_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added, False if the log has reached its size limit.
    """
    # Basic input validation to guard against accidental injection of control characters
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Trim excessively long strings to prevent runaway memory usage
    user_name = user_name.strip()[:256]
    event_description = event_description.strip()[:2048]

    # Create the log entry
    entry = {
        "user_name": user_name,
        "event_description": event_description,
        # Using a timestamp helps with auditing and analytics
        "timestamp": threading.current_thread().name  # placeholder for actual timestamp
    }

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; reject new entries to avoid uncontrolled growth
            return False
        activity_log.append(entry)

    return True