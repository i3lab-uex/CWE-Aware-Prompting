import datetime
import threading

# Global list to store user activity logs
activity_log = []
# A lock to ensure thread‑safe writes to the global list
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a new user activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging succeeded, False otherwise.
    """
    # Basic validation to avoid corrupt entries
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    entry = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    try:
        with _activity_lock:
            activity_log.append(entry)
    except Exception:
        # In a real system we might log this error to a file or monitoring service
        return False

    return True