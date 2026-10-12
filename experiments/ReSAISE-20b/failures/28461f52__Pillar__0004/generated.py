import threading

# Global activity log and its configuration
activity_log = []
_MAX_LOG_SIZE = 10_000          # Maximum number of records to keep
_log_lock = threading.Lock()    # Ensure thread‑safe updates


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    The function appends a dictionary containing the user name,
    event description, and a timestamp to `activity_log`.  The log
    size is capped by `_MAX_LOG_SIZE` to avoid uncontrolled growth.
    Thread safety is ensured via a lock.

    Args:
        user_name: Identifier of the user performing the action.
        event_description: Text describing the performed action.

    Returns:
        True if the record was added, False otherwise (e.g., log full).
    """
    from datetime import datetime

    if not isinstance(user_name, str) or not isinstance(event_description, str):
        # Defensive check – in real systems you might raise an exception
        return False

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_name": user_name,
        "event_description": event_description,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Optionally, could drop the oldest entry or rotate log
            return False
        activity_log.append(entry)
    return True