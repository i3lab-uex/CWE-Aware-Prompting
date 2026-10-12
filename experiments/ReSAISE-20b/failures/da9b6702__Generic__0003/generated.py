import threading
from datetime import datetime

# Global activity log repository
activity_log = []

# Thread‑safety lock for concurrent access
_activity_lock = threading.Lock()

# Maximum allowed entries in the activity log
_MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action performed.

    Returns
    -------
    bool
        ``True`` if the event was logged successfully,
        ``False`` if the log size limit was exceeded and the
        operation was aborted.
    """
    # Basic validation to avoid accidental injection of newline or
    # other control characters that could break log formatting.
    if not user_identifier or not task:
        return False

    # Ensure thread safety when modifying the global log
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entry
            return False

        # Construct a single log record with timestamp.
        # Using ISO 8601 format for unambiguous ordering and parsing.
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_identifier,
            "action": task
        }

        activity_log.append(record)
    return True