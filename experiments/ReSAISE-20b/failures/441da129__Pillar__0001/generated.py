import threading
from datetime import datetime

# Global activity log and its configuration
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()
_MAX_LOG_ENTRIES = 10_000   # maximum number of entries to retain


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the event was logged, False if the log is full and the
        attempt was rejected.

    Notes
    -----
    - Thread‑safety is ensured via a global lock.
    - The function enforces an upper bound on the log size to avoid
      uncontrolled growth (CWE‑664 consideration).
    """
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        raise TypeError("user_key and action_details must be strings")

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Reject logging to prevent resource exhaustion
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(entry)
        return True