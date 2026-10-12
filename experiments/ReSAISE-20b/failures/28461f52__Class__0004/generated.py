import threading

# Global activity log and its maximum allowed size
activity_log: list[tuple[str, str]] = []
MAX_LOG_SIZE = 10_000

# Lock to guard concurrent modifications of the log
_log_lock = threading.Lock()


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user.
    event_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log is already at its
        maximum capacity.

    Notes
    -----
    * The function guards against uncontrolled growth of the log
      (CWE‑400) by enforcing a hard limit on the number of entries.
    * Thread safety is achieved using a lock so that concurrent
      calls do not corrupt the list or bypass the size check.
    """
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        # Store a tuple of (user_name, event_description)
        activity_log.append((user_name, event_description))
    return True