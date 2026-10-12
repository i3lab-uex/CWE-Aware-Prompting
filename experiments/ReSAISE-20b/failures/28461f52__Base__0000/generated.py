import threading

# Global activity log and lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries in the log to mitigate CWE‑770
_MAX_LOG_ENTRIES = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user performing the action.
    event_description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the entry was added; False if the log limit was reached.

    Notes
    -----
    * The function is thread‑safe via a global lock.
    * The log size is capped at ``_MAX_LOG_ENTRIES`` to avoid uncontrolled
      memory consumption (CWE‑770).
    """
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        # Basic type validation – silently ignore invalid input
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Log is full; do not add new entry
            return False

        # Append a timestamped record for auditability
        import datetime
        activity_log.append({
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'user': user_name,
            'event': event_description
        })
    return True