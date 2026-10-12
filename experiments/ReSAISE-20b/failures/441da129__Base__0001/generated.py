import threading
from datetime import datetime

# Global activity log and a lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed (configurable)
_MAX_LOG_ENTRIES = 10_000

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier of the user performing the action.
    action_details : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the event was logged successfully; False if the log is full.
    """
    # Basic validation
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    # Create a log entry with timestamp
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_key": user_key,
        "action_details": action_details
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Log is full – reject new entries to avoid unbounded growth
            return False

        activity_log.append(entry)

    return True