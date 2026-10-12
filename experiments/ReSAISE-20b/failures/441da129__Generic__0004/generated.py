import threading
from datetime import datetime

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Optional: maximum allowed entries in the log to prevent uncontrolled growth
_MAX_LOG_SIZE = 10_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged, False if the log is full.

    Notes
    -----
    - The function uses a global lock to protect concurrent writes.
    - Each log entry is a dictionary containing the timestamp, user key,
      and action details. This structure keeps the log extensible
      (e.g., you can later add IP addresses or session IDs).
    - No exceptions are raised; the caller should check the return value.
    """
    # Basic input validation
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        # Silently reject invalid input as per "Raise: None"
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(entry)

    return True