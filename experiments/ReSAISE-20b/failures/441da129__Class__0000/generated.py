import time
from threading import Lock

# Global activity log and its lock for thread‑safety
activity_log: list[dict] = []
_activity_lock = Lock()

# Maximum number of entries allowed in the log
_MAX_LOG_SIZE: int = 10_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier of the user performing the action.
    action_details : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was recorded, False if the log is at capacity.
    """
    # Simple size check to avoid uncontrolled growth (CWE‑400)
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        record = {
            "timestamp": time.time(),
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(record)
    return True