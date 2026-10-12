import datetime
import threading

# Global activity log and a lock for thread‑safe access
activity_log: list[dict] = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log
_MAX_LOG_SIZE: int = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        ``True`` if the action was successfully recorded,
        ``False`` if the log is already at its maximum capacity.
    """
    # Quick check to avoid unnecessary locking
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "event": event,
    }

    with _activity_lock:
        # Re‑check inside the lock to guard against race conditions
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(entry)

    return True