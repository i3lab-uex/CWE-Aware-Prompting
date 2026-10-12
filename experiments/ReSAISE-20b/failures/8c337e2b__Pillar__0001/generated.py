import threading
from datetime import datetime
from typing import List, Dict

# Global activity log and its associated lock to prevent race conditions.
activity_log: List[Dict[str, str]] = []
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global activity_log.

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
    # Basic validation to avoid corrupt entries.
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False
    if user_id.strip() == "" or action.strip() == "":
        return False

    # Create the log entry.
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "action": action,
    }

    # Append the entry atomically to avoid concurrent modification issues.
    try:
        with _activity_lock:
            activity_log.append(entry)
        return True
    except Exception:
        # In a real system you might log this exception to an error monitoring service.
        return False