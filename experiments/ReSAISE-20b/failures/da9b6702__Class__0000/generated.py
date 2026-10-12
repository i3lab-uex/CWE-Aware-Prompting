import threading

# Global activity log and its lock for thread‑safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed number of entries to avoid uncontrolled resource consumption.
_MAX_LOG_SIZE = 10_000

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the event was successfully logged, False if the log size limit would be exceeded.
    """
    # Basic input validation to avoid storing nonsensical data.
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Truncate overly long strings to keep the log compact.
    user_identifier = user_identifier[:256]
    task = task[:1024]

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not append; return False to signal failure.
            return False
        activity_log.append({
            'user': user_identifier,
            'task': task,
        })
    return True