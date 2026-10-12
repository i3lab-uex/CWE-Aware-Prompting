import threading

# Global activity log list and a lock for thread‑safety
activity_log: list[dict[str, str]] = []
_activity_lock = threading.Lock()

# Maximum allowed number of log entries (prevent CWE‑770)
_MAX_LOG_SIZE = 10_000


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier of the user performing the action.
    action_details : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log has reached its size limit.
    """
    # Quick pre‑check to avoid acquiring lock if we are already over the limit
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    with _activity_lock:
        # Double‑check inside the lock
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        # Record structure: timestamp could be added here if needed
        activity_log.append({"user_key": user_key, "action_details": action_details})
    return True