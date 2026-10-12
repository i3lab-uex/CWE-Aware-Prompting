import threading

# Global activity log storage
activity_log = []
# Maximum number of entries allowed in the log to avoid uncontrolled growth
_MAX_LOG_SIZE = 1000

# Lock to ensure thread‑safe modifications of the log
_log_lock = threading.Lock()


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier of the user who performed the action.
    event_description : str
        Textual description of the action taken.

    Returns
    -------
    bool
        True if the entry was added successfully, False if it was not
        added due to exceeding the maximum log size or invalid input.
    """
    # Basic type validation
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Construct the log entry
    entry = {
        "user_name": user_name,
        "event_description": event_description,
        # Store a timestamp for audit purposes
        "timestamp": _current_timestamp(),
    }

    with _log_lock:
        # Prevent uncontrolled growth of the log
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)

    return True


def _current_timestamp() -> str:
    """Return an ISO‑8601 formatted UTC timestamp."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()