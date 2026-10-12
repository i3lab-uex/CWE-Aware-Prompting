import threading

# Global activity log and a lock to guard concurrent access.
activity_log = []
_log_lock = threading.Lock()

# Maximum number of records allowed in the log to prevent uncontrolled growth.
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    event : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the record was appended successfully.
        False if the log has reached its maximum size and the
        operation is rejected to avoid uncontrolled resource consumption.
    """
    # Basic validation: ensure inputs are strings and not excessively long.
    if not isinstance(uid, str) or not isinstance(event, str):
        return False
    # Optionally truncate very long strings to a sane limit (e.g., 256 chars).
    uid = uid[:256]
    event = event[:1024]

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entries to prevent uncontrolled growth.
            return False

        activity_log.append({
            "uid": uid,
            "event": event,
            "timestamp": __import__("time").time()
        })
    return True