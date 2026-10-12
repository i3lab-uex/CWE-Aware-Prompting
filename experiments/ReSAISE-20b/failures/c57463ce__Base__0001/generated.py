import datetime
import threading

# Global activity log (list of dictionaries)
activity_log = []

# Optional maximum number of entries to avoid uncontrolled growth
MAX_LOG_SIZE = 10_000

# Lock for thread‑safe updates to the activity log
_log_lock = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Register a user event in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was added to the log; False if the log has reached its size limit.
    """
    # Basic validation
    if not isinstance(uid, str) or not isinstance(description, str):
        raise TypeError("uid and description must be strings")

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject logging to prevent unbounded growth
            return False

        event = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "uid": uid,
            "description": description,
        }
        activity_log.append(event)
    return True