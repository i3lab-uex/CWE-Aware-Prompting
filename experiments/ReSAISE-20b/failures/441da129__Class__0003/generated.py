import threading

# Global activity log and its configuration
activity_log: list[dict[str, str]] = []
_MAX_LOG_SIZE = 10_000   # maximum number of entries allowed
_log_lock = threading.Lock()


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user event in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user.
    action_details : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the event was logged; False if the log has reached its maximum size.
    """
    # Basic validation to avoid malicious input
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    # Enforce log size limit to mitigate CWE-400
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        # Append a new entry
        activity_log.append({
            "user_key": user_key,
            "action_details": action_details
        })
    return True