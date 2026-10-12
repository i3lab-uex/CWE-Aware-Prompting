import threading

# Global activity log and its lock for thread‑safety
activity_log: list[tuple[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of log entries to keep in memory
_MAX_LOG_SIZE: int = 10_000

def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added successfully, False otherwise.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    # Construct the log entry
    entry = (user_id, action)

    with _activity_lock:
        # Enforce a maximum size to mitigate CWE-770
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Remove the oldest entry (FIFO)
            activity_log.pop(0)

        try:
            activity_log.append(entry)
        except Exception:
            # Any unexpected failure is reported as False
            return False

    return True