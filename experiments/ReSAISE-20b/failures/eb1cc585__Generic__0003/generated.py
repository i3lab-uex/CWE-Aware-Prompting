import datetime
from typing import List, Dict

# Global activity log and a lock for thread‑safety
activity_log: List[Dict[str, str]] = []
_LOG_LOCK = None  # will be initialized lazily
_MAX_LOG_SIZE = 10_000   # maximum number of entries allowed

def _ensure_lock() -> None:
    """Create a lock object if it doesn't exist yet."""
    global _LOG_LOCK
    if _LOG_LOCK is None:
        import threading
        _LOG_LOCK = threading.Lock()

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    _ensure_lock()
    with _LOG_LOCK:
        # Reject if the log has reached its maximum size
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        # Append a new log entry
        activity_log.append({
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user_identifier": user_identifier,
            "event": event
        })
    return True