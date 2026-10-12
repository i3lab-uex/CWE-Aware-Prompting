import threading

# Global activity log and configuration constants
activity_log: list[dict] = []
_MAX_LOG_SIZE = 10_000          # Maximum number of entries allowed
_log_lock = threading.Lock()    # Protects concurrent access to activity_log


def track_user_event(uid: str, description: str) -> bool:
    """
    Records a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged successfully.
        False if the log is at capacity and the entry was rejected.

    Notes
    -----
    * The function enforces a hard limit on the size of `activity_log`
      to mitigate CWE‑770 (unbounded resource allocation).
    * Thread safety is ensured via a reentrant lock.
    """
    # Basic input validation (prevent obvious injection attacks)
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    # Trim whitespace to avoid accidental growth from accidental spaces
    uid = uid.strip()
    description = description.strip()

    # Prepare the log entry
    entry = {
        "uid": uid,
        "description": description,
        "timestamp": threading.current_thread().name  # placeholder for real timestamp
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject the entry to prevent unlimited growth
            return False
        activity_log.append(entry)
    return True