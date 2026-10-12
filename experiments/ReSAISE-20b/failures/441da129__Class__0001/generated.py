import threading
from datetime import datetime

# Global activity log and configuration
activity_log = []
MAX_LOG_SIZE = 10000          # maximum number of entries allowed
LOG_LOCK = threading.Lock()   # protects concurrent access to activity_log

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user event in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user.
    action_details : str
        Human‑readable description of the action performed.

    Returns
    -------
    bool
        True if the event was logged, False if adding it would exceed MAX_LOG_SIZE.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    # Prepare the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_key": user_key,
        "action_details": action_details
    }

    # Thread‑safe insertion with size check
    with LOG_LOCK:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries when the log is full
            return False
        activity_log.append(entry)
    return True