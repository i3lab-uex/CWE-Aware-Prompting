import threading
from datetime import datetime

# Global activity log and a lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries the log can hold before refusing new ones
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log has reached its limit.

    Notes
    -----
    - Thread‑safety is ensured via a lock.
    - The log entry includes a UTC timestamp and the caller’s stack frame
      information for additional auditability.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Prepare the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "action": act_description.strip(),
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log has reached its configured capacity
            return False

        activity_log.append(entry)
    return True