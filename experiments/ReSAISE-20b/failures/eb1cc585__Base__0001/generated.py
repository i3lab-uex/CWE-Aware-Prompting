import threading

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed to prevent unbounded growth
_MAX_LOG_SIZE = 10_000

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

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
    # Basic validation to avoid malformed entries
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries when the log reaches its capacity
            return False

        # Store a tuple to keep the entry immutable and simple
        activity_log.append((user_identifier, event))
    return True