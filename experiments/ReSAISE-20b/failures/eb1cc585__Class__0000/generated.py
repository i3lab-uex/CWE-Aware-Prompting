import threading

# Global activity log and its configuration
activity_log: list[tuple[str, str]] = []
LOG_MAX_SIZE: int = 1000   # maximum number of entries allowed
_log_lock = threading.Lock()  # protects concurrent access to activity_log


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Records a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Human‑readable description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    # Basic validation to avoid accidental injection of newlines
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Ensure the log does not exceed its configured maximum size
    with _log_lock:
        if len(activity_log) >= LOG_MAX_SIZE:
            return False
        activity_log.append((user_identifier, event))
    return True