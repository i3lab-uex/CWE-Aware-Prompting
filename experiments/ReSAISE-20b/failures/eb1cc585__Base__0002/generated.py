import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety
activity_log: list[tuple[str, str, datetime]] = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the activity log.
_MAX_LOG_SIZE = 10_000


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
        True if the entry was added, False if the log is at capacity.
    """
    # Basic input validation
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        raise TypeError("user_identifier and event must be strings")

    # Acquire lock to prevent race conditions in a multi‑threaded environment
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject the new entry
            return False

        # Append a tuple containing user ID, event description and timestamp
        activity_log.append((user_identifier, event, datetime.utcnow()))
        return True