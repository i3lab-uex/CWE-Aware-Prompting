import threading
from datetime import datetime

# Global activity log and a lock for thread‑safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the log (to avoid uncontrolled growth)
_MAX_LOG_ENTRIES = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user who performed the action.
    event_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was added successfully, False if the log has reached its maximum size.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Construct the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_name": user_name,
        "event_description": event_description,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Do not add new entry; resource limit reached
            return False

        activity_log.append(entry)
        return True