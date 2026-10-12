import threading

# Global activity log and its mutex for thread‑safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries the log can hold before rejecting new ones
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    act_description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log is full.
    """
    # Basic validation: ensure both arguments are strings
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Optionally strip whitespace to avoid accidental duplicates or overly long strings
    uid_clean = uid.strip()
    act_clean = act_description.strip()

    if not uid_clean or not act_clean:
        return False

    with _log_lock:
        # Enforce the maximum size limit
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        # Append a new record as a dictionary
        activity_log.append({
            "uid": uid_clean,
            "action": act_clean,
            # Use a timestamp for auditability
            "timestamp": _current_timestamp()
        })

    return True

def _current_timestamp() -> float:
    """Return the current time as a UNIX timestamp in seconds."""
    import time
    return time.time()