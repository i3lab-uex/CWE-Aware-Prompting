import datetime
from typing import List, Dict

# Global activity log and lock for thread safety
activity_log: List[Dict[str, str]] = []
LOG_LOCK = None  # will be initialized lazily

# Optional maximum number of entries to keep in the log
MAX_LOG_SIZE = 10_000


def _ensure_lock() -> None:
    """Initialize the global lock if it hasn't been created yet."""
    global LOG_LOCK
    if LOG_LOCK is None:
        import threading  # local import to avoid unnecessary dependency at module load
        LOG_LOCK = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was logged; False if the log is full.
    """
    _ensure_lock()

    # Basic validation
    if not isinstance(uid, str) or not isinstance(description, str):
        raise TypeError("uid and description must be strings")

    # Create the log entry
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    with LOG_LOCK:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(entry)

    return True