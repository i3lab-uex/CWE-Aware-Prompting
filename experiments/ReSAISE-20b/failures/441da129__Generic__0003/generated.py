import threading

# Global activity log and associated lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log.  Adjust as needed.
_MAX_LOG_SIZE = 10_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user event in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was added to the log, False if the maximum size limit
        prevented logging.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    entry = {"user_key": user_key, "action_details": action_details}

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; reject the new entry
            return False
        activity_log.append(entry)

    return True