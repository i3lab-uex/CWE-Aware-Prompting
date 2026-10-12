import threading

# Global activity log storage
activity_log: list[dict[str, str]] = []

# Maximum number of entries allowed in the log
_MAX_LOG_SIZE = 10_000

# Thread‑safe lock for concurrent access
_log_lock = threading.Lock()


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user who performed the action.
    event_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log has reached its
        maximum allowed size and the entry was rejected.
    """
    # Basic validation: ensure non‑empty strings
    if not user_name or not event_description:
        return False

    # Prepare the log entry
    entry = {"user": user_name, "event": event_description}

    with _log_lock:
        # Enforce the maximum log size to avoid uncontrolled resource consumption
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)
        return True