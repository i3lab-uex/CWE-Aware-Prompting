import datetime
from threading import Lock

# Global list to store user activity logs
activity_log = []
# A lock to ensure thread‑safe updates to the global list
_log_lock = Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Log a user activity by appending an entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging was successful, False otherwise.
    """
    try:
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            # To avoid storing raw user input that could break formatting or
            # expose sensitive data, escape control characters.
            "action": action.replace("\n", "\\n").replace("\r", "\\r"),
        }
    except Exception:
        # Any error constructing the entry should cause a failure return
        return False

    try:
        with _log_lock:
            activity_log.append(entry)
        return True
    except Exception:
        # If appending fails (unlikely but possible if memory is exhausted),
        # return False.
        return False