import datetime
from threading import Lock

# Global activity log and a lock for thread‑safety
activity_log = []
_log_lock = Lock()

# Optional size limit to prevent unbounded growth
MAX_LOG_SIZE = 100_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user event in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged; False if the log is at capacity.
    """
    # Basic validation
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; reject the new entry
            return False

        event = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(event)
    return True