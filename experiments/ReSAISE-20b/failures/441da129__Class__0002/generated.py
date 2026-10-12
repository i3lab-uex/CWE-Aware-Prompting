import threading
from datetime import datetime

# Global activity log and lock for thread‑safe access
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed to prevent uncontrolled resource consumption
_MAX_LOG_ENTRIES = 10_000

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user event in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log is full.
    """
    # Basic input validation to avoid malformed entries
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    # Construct the log entry with a timestamp for auditability
    entry = {
        'timestamp': datetime.utcnow().isoformat() + "Z",
        'user_key': user_key,
        'action_details': action_details
    }

    with _activity_lock:
        # Prevent uncontrolled growth of the log (CWE‑400)
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            return False
        activity_log.append(entry)
    return True