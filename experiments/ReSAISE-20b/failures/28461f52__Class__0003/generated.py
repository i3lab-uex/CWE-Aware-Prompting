import threading

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries in the activity log to prevent uncontrolled resource consumption
_MAX_LOG_ENTRIES = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user.
    event_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the event was logged, False if adding it would exceed _MAX_LOG_ENTRIES.
    """
    # Basic validation to avoid logging empty or non-string values
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False
    if user_name.strip() == "" or event_description.strip() == "":
        return False

    # Build the log entry
    entry = {
        "user": user_name,
        "event": event_description,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    with _activity_lock:
        # Enforce maximum size constraint
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            return False

        activity_log.append(entry)

    return True