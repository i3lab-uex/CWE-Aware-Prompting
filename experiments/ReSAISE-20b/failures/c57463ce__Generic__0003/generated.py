import datetime
import threading

# Global activity log and its lock for thread‑safety
activity_log = []
_LOG_LOCK = threading.Lock()
# Maximum number of log entries allowed (adjust as needed)
_MAX_LOG_SIZE = 10_000

def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user event in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the event was logged successfully,
        False if the log size limit has been reached.
    """
    # Basic validation
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    # Prepare the log entry
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject logging to prevent uncontrolled growth
            return False
        activity_log.append(entry)

    return True