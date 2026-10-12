import threading
from datetime import datetime

# Global activity log and lock for thread‑safety (CWE‑664 mitigation)
activity_log: list[dict] = []
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global activity_log.

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
    try:
        # Basic input validation: ensure strings and strip whitespace
        if not isinstance(user_id, str) or not isinstance(action, str):
            return False

        user_id = user_id.strip()
        action = action.strip()

        if not user_id or not action:
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "action": action,
        }

        # Protect the shared resource with a lock
        with _activity_lock:
            activity_log.append(entry)

        return True

    except Exception:
        # Any unexpected error should not crash the caller
        return False