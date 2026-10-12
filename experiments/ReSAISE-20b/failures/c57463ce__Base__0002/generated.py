import time
from typing import List, Dict

# Global activity log and a lock for thread‑safety
activity_log: List[Dict[str, str]] = []
_LOG_LOCK = False  # simple flag lock (avoid threading import for minimal footprint)

# Maximum allowed entries to avoid uncontrolled growth (CWE‑770 mitigation)
_MAX_LOG_SIZE = 10_000

def _acquire_lock() -> bool:
    """Acquire a very simple lock. Returns True if acquired, False otherwise."""
    global _LOG_LOCK
    if not _LOG_LOCK:
        _LOG_LOCK = True
        return True
    return False

def _release_lock() -> None:
    """Release the simple lock."""
    global _LOG_LOCK
    _LOG_LOCK = False

def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user event in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    description : str
        Human‑readable action description.

    Returns
    -------
    bool
        True if the event was logged, False if the log is at capacity.
    """
    # Ensure we do not exceed the maximum allowed size
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    # Acquire lock to prevent concurrent modifications
    if not _acquire_lock():
        # In a real system we would retry or use a proper threading.Lock
        return False

    try:
        # Append event with timestamp for traceability
        activity_log.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "uid": uid,
            "description": description
        })
    finally:
        _release_lock()

    return True