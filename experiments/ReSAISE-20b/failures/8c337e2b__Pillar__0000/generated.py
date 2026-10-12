import threading

# Global list to store user activity logs
activity_log = []

# Lock to ensure thread‑safe access to the log
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a new user activity entry to the global activity_log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    # Build the log entry (timestamp can be added if needed)
    entry = {"user_id": user_id, "action": action}

    try:
        # Ensure exclusive access to the shared resource
        with _activity_lock:
            activity_log.append(entry)
    except Exception:
        # Fail silently as per specification
        return False

    return True