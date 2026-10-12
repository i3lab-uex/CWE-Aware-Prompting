import threading

# Global activity log and its lock for thread‑safety
activity_log: list[dict] = []
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global activity_log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the log entry was added successfully, False otherwise.
    """
    # Basic validation to avoid logging meaningless entries
    if not user_id or not action:
        return False

    entry = {"user_id": user_id, "action": action}

    # Protect the shared resource with a lock to prevent race conditions
    try:
        with _activity_lock:
            activity_log.append(entry)
        return True
    except Exception:
        # In the unlikely event of an error, do not propagate it
        return False