import threading

# Global activity log with a predefined maximum size to avoid uncontrolled resource consumption.
MAX_LOG_SIZE = 10_000
activity_log = []
_log_lock = threading.Lock()


def record_user_action(uid: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the activity was logged successfully,
        False if the log has reached its maximum size.
    """
    # Basic input validation to guard against malformed data.
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Acquire the lock to ensure thread‑safe modifications.
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Do not add new entries once the limit is reached.
            return False
        # Append a tuple to keep the structure simple and immutable.
        activity_log.append((uid, event))
    return True