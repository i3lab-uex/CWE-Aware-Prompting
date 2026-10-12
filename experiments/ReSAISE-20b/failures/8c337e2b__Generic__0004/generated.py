import threading
from datetime import datetime

# Global list to store activity logs
activity_log: list[dict] = []

# Thread‑safety lock for concurrent access to the log
_log_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the entry was appended successfully, False otherwise.
    """
    try:
        # Basic validation to avoid empty or None values
        if not user_id or not action:
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "action": action,
        }

        # Ensure atomic append in a multi‑threaded environment
        with _log_lock:
            activity_log.append(entry)

        return True

    except Exception:
        # No exception should be raised; failure is indicated by False
        return False