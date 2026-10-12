import threading

# Global activity log and its configuration
activity_log = []
_ACTIVITY_LOG_LOCK = threading.Lock()
_MAX_ACTIVITY_LOG_SIZE = 10_000   # Maximum number of entries allowed

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action performed by the user.

    Returns
    -------
    bool
        True if the event was logged successfully; False if the log has reached its size limit.

    Notes
    -----
    - The function is thread‑safe and will not raise exceptions.
    - A global size limit prevents unbounded memory growth (CWE‑770 mitigation).
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Prepare the log entry
    entry = {
        "user_identifier": user_identifier,
        "task": task,
        "timestamp": _current_timestamp()
    }

    # Safely update the log with a lock
    with _ACTIVITY_LOG_LOCK:
        if len(activity_log) >= _MAX_ACTIVITY_LOG_SIZE:
            # Log size limit reached – reject new entry
            return False

        activity_log.append(entry)
    return True


def _current_timestamp() -> str:
    """Return the current UTC timestamp as an ISO‑8601 string."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()