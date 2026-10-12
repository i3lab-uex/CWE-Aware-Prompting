import threading

# Global activity log and a maximum size limit to prevent unbounded growth.
activity_log = []
MAX_LOG_SIZE = 10_000          # Adjust as appropriate for your environment.
_log_lock = threading.Lock()   # Ensure thread‑safe updates to the log.

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully; False if the log has reached its
        configured maximum size and the event could not be stored.
    """
    # Basic validation to avoid storing malformed entries
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Construct the record; timestamp can be added if desired.
    record = {"user": user_identifier, "task": task}

    with _log_lock:
        # Enforce the size limit to mitigate CWE‑770
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        activity_log.append(record)
        return True