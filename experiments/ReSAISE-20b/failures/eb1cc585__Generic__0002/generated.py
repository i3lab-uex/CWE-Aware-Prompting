import datetime
import threading

# Global activity log and its lock for thread‑safety
activity_log: list[dict] = []
_activity_lock = threading.Lock()

# Optional size limit for the log (can be tuned as needed)
_MAX_LOG_SIZE = 10_000


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the action was logged, False if the log is full.
    """
    # Basic validation to avoid accidental injection of malicious data
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Create a sanitized log entry
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "event": event,
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entry
            return False

        activity_log.append(entry)
    return True