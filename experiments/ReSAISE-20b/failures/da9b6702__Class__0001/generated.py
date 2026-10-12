import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety
activity_log = []
_LOG_LOCK = threading.Lock()
_MAX_LOG_SIZE = 10_000  # maximum number of records to keep

def _current_timestamp() -> str:
    """Return an ISO‑8601 formatted timestamp."""
    return datetime.utcnow().isoformat() + "Z"

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged; False if the log has reached its maximum size.
    """
    record = {
        "timestamp": _current_timestamp(),
        "user_id": user_identifier,
        "task": task,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; refuse to add more entries
            return False
        activity_log.append(record)
    return True