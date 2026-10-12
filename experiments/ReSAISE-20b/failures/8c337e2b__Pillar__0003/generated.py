import threading

# Global list to store user activity logs
activity_log = []

# Lock to ensure thread‑safe access to the global list
_activity_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was appended successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    # Construct the log entry
    entry = {
        "user_id": user_id,
        "action": action,
        "timestamp": _current_timestamp(),
    }

    try:
        # Ensure exclusive access to the shared resource
        with _activity_lock:
            activity_log.append(entry)
    except Exception:
        # In the unlikely event of an error, do not raise – just signal failure
        return False

    return True


def _current_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.
    This helper keeps the log entries consistent and avoids exposing
    local time details that could be misinterpreted.
    """
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()