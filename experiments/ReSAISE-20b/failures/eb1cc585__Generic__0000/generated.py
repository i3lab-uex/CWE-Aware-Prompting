import threading

# Global activity log and its lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries the log can hold.
MAX_LOG_SIZE = 10_000


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Append a user action to the global activity log.

    Parameters
    ----------
    user_identifier : str
        A unique string identifier for the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log is at capacity.
    """
    # Basic validation to avoid storing malformed entries
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Enforce a maximum log size
    with _activity_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append((user_identifier, event))
    return True