import threading
from datetime import datetime

# Global activity log and its lock for thread safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries the log can hold (adjust as needed)
_MAX_LOG_ENTRIES = 10_000

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Records a user action in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user.
    action_details : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log size limit was reached.
    """
    # Basic validation
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    with _log_lock:
        # Enforce size limit to avoid uncontrolled growth
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            return False

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(entry)

    return True