import datetime
import threading

# Global activity log and its maximum allowed size to prevent uncontrolled resource consumption.
activity_log = []
_MAX_LOG_SIZE = 100_000
_log_lock = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log size limit prevented logging.
    """
    # Ensure that uid and description are strings; otherwise, treat as invalid input
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    # Prepare the log entry
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    # Append the entry in a thread‑safe manner
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries once the limit is reached to avoid uncontrolled growth
            return False
        activity_log.append(entry)

    return True