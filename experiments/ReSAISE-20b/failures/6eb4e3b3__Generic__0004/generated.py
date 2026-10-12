import time
from typing import List, Tuple

# Global activity log and a lock for thread‑safety
activity_log: List[Tuple[str, str, float]] = []
_MAX_LOG_SIZE = 10_000          # maximum number of records allowed
_log_lock = None                # will be initialised lazily

def _ensure_lock() -> None:
    """Initialise the lock on first use to avoid global import side‑effects."""
    global _log_lock
    if _log_lock is None:
        from threading import Lock
        _log_lock = Lock()

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was appended, False if the log size limit was reached.
    """
    # Validate inputs
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    _ensure_lock()
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        # Store a tuple of (uid, event, timestamp)
        activity_log.append((uid, event, time.time()))
    return True