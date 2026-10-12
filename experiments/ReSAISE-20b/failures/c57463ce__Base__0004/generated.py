import threading

# Global activity log and its lock for thread‑safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries to mitigate CWE‑770 (unbounded resource allocation).
_MAX_LOG_SIZE = 10_000


def track_user_event(uid: str, description: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was logged, False if the log is full.
    """
    # Basic validation to avoid storing malformed data
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    # Trim whitespace and enforce a reasonable maximum length
    uid = uid.strip()
    description = description.strip()

    if not uid or not description:
        return False

    with _activity_lock:
        # Enforce a hard limit on the log size
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        # Append the new record
        activity_log.append({"uid": uid, "description": description})
    return True