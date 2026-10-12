import threading

# Global activity log and its associated lock for thread safety
activity_log: list[dict[str, str]] = []
_activity_lock = threading.Lock()

# Define a sensible maximum number of log entries to avoid unbounded growth
_MAX_LOG_SIZE = 10_000

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Records a user event into the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user.
    action_details : str
        Description of the user's action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log has reached its maximum size.
    """
    # Validate inputs (basic type checks; further validation could be added as needed)
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        raise TypeError("user_key and action_details must be strings")

    # Ensure thread-safe access to the shared log
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject logging to prevent unbounded growth
            return False

        # Append the new event record
        activity_log.append({
            "user_key": user_key,
            "action_details": action_details
        })
    return True