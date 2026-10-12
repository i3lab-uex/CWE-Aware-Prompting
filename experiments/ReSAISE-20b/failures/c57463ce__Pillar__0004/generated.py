import threading
from datetime import datetime

# Global activity log and its configuration
activity_log = []
MAX_LOG_SIZE = 10_000          # maximum allowed entries
_log_lock = threading.Lock()   # ensures thread‑safe updates

def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged; False if the log is full.

    Notes
    -----
    * Thread safety is ensured via a lock.
    * The function does not raise exceptions; it simply returns False when the log
      would exceed its configured maximum size.
    """
    # Basic input validation
    if not isinstance(uid, str) or not isinstance(description, str):
        raise TypeError("uid and description must be strings")

    # Prepare the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject logging to prevent uncontrolled growth
            return False

        activity_log.append(entry)
    return True