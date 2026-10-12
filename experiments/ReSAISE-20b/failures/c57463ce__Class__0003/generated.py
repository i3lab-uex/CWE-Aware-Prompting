import threading
from datetime import datetime

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries to prevent uncontrolled resource consumption (CWE-400)
MAX_LOG_SIZE = 10_000

def track_user_event(uid: str, description: str) -> bool:
    """
    Records a user event in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Human‑readable description of the event.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log is full.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(description, str) or not description:
        return False

    # Prepare the log entry with a timestamp
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description
    }

    with _activity_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries when the log is full
            return False

        activity_log.append(entry)
    return True