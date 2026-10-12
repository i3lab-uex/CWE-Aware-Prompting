import threading

# Global activity log and its lock for thread safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log.
_MAX_LOG_SIZE = 10_000

def track_user_operation(account: str, operation: str) -> bool:
    """
    Record a user activity in the global `activity_log`.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        ``True`` if the activity was logged successfully.
        ``False`` if the log has reached its maximum size and
        the operation was not recorded.
    """
    # Basic validation to avoid storing empty or excessively long strings.
    if not account or not operation:
        return False

    # Truncate overly long entries to keep the log size predictable.
    account = account[:256]
    operation = operation[:1024]

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; refuse to append.
            return False
        activity_log.append((account, operation))
    return True