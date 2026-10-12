import threading

# Global activity log list and its lock for thread safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the activity log.
_MAX_LOG_SIZE = 10_000


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log is full.
    """
    # Basic validation to avoid storing empty or malformed data
    if not user_identifier or not event:
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entries to prevent uncontrolled growth.
            return False
        activity_log.append((user_identifier, event))
    return True