import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety.
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the log to prevent uncontrolled growth.
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was added, False if adding would exceed the log size limit.
    """
    # Validate inputs are strings; silently convert otherwise.
    uid = str(uid)
    event = str(event)

    # Create the record with a timestamp.
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "event": event
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject the new entry to enforce size limit.
            return False
        activity_log.append(record)
    return True