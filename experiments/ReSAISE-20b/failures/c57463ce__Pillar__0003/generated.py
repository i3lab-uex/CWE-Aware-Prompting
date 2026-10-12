import threading

# Global activity log list and its associated lock for thread‑safety.
activity_log = []
_activity_lock = threading.Lock()

# Optional configuration: maximum allowed entries in the activity log.
_MAX_LOG_SIZE = 10_000

def track_user_event(uid: str, description: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        ``True`` if the event was logged successfully.
        ``False`` if the log size limit was reached and the event
        was rejected.

    Notes
    -----
    * The function is thread‑safe; concurrent calls will not corrupt the log.
    * No exceptions are raised. Invalid input types are silently ignored
      and result in a ``False`` return value.
    * The log size is capped by :data:`_MAX_LOG_SIZE` to avoid unbounded
      memory consumption, addressing CWE‑664 concerns.
    """
    # Basic type validation – avoid storing malformed entries.
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries once the limit is reached.
            return False

        activity_log.append({
            "uid": uid,
            "description": description
        })
    return True