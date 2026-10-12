import datetime
from threading import Lock

# Global activity log and a lock for thread‑safe updates
activity_log = []
_activity_lock = Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the log entry was appended successfully, False otherwise.
    """
    try:
        timestamp = datetime.datetime.utcnow().isoformat()
        entry = {"user_id": user_id, "action": action, "timestamp": timestamp}
        with _activity_lock:
            activity_log.append(entry)
        return True
    except Exception:
        # In a real system we might log this exception somewhere.
        return False