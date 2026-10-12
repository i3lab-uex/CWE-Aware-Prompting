import time
from threading import Lock

# Global activity log and its lock for thread safety
activity_log = []
_log_lock = Lock()

# Maximum number of entries the log can hold. Adjust as needed.
MAX_LOG_SIZE = 10_000

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was logged successfully, False if the log is full.
    """
    # Ensure arguments are strings; silently coerce to string to avoid errors
    user_identifier = str(user_identifier)
    event = str(event)

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log size limit reached; reject new entry
            return False

        entry = {
            "timestamp": time.time(),  # Unix epoch seconds
            "user_id": user_identifier,
            "event": event
        }
        activity_log.append(entry)
    return True