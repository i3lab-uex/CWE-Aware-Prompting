import time
from datetime import datetime
from threading import Lock

# Global activity log and its configuration
activity_log: list[dict] = []
_MAX_LOG_SIZE: int = 10_000          # Maximum number of entries allowed
_log_lock = Lock()                   # Ensure thread‑safe modifications

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log has reached its
        configured size limit.
    """
    global activity_log

    # Quick check to avoid acquiring the lock if we already know the limit is reached
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    # Build the log entry
    record = {
        "uid": uid,
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # Append in a thread‑safe manner
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:   # Re‑check inside the lock
            return False
        activity_log.append(record)

    return True