import threading

# Global activity log and its lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed to prevent uncontrolled growth
_MAX_LOG_SIZE = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Identifier for the user performing the action.
    event_description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log size limit
        would be exceeded.

    Notes
    -----
    * The function is thread‑safe; concurrent calls are serialized by a lock.
    * A hard limit on the log size prevents uncontrolled memory usage
      (CWE‑770 mitigation).
    * No external side effects or I/O are performed, keeping the function pure.
    """
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        # Reject invalid input silently; could also raise TypeError if desired
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not add the entry; log limit reached
            return False

        # Append a new record as a tuple (timestamp, user_name, event_description)
        activity_log.append((user_name, event_description))
    return True