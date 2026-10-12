import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries the log may hold before refusing new records
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
        True if the record was added; False if the log has reached its size limit.
    """
    # Quick size check before acquiring lock to reduce contention
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    # Build the record
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "event": event
    }

    # Safely append to the global log
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(record)

    return True