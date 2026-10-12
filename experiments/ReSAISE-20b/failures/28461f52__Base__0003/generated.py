import threading

# Global activity log and a lock to make it thread‑safe
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the activity log
_MAX_LOG_ENTRIES = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Add a user activity record to the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier of the user.
    event_description : str
        Human‑readable description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if it would exceed the maximum log size.
    """
    # Quick sanity checks to avoid storing empty data
    if not user_name or not event_description:
        return False

    # Build the log entry
    entry = {
        "user": user_name,
        "event": event_description,
        # Store a timestamp for future reference
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Do not add the entry to prevent unbounded growth
            return False

        activity_log.append(entry)
    return True