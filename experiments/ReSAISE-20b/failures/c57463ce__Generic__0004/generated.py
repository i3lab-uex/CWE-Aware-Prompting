import threading

# Global activity log and a lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Optional limit on the number of entries to prevent unbounded growth
_MAX_LOG_SIZE = 10000

def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    description : str
        Human‑readable text describing the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    # Basic input validation to guard against malformed data
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    # Truncate overly long strings to avoid abuse
    uid = uid.strip()[:256]
    description = description.strip()[:1024]

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append({"uid": uid, "description": description})
    return True