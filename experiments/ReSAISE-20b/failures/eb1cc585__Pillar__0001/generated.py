import threading

# Global activity log list
activity_log = []

# Maximum number of entries allowed in the log to prevent uncontrolled growth.
MAX_LOG_SIZE = 10_000

# Thread‑safety lock for concurrent modifications
_log_lock = threading.Lock()


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added to the log, False if the log is at capacity.
    """
    # Basic validation of inputs
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject logging to prevent uncontrolled resource usage
            return False

        activity_log.append((user_identifier, event))
    return True