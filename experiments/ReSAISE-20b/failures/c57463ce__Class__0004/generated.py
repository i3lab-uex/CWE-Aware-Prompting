import datetime
import threading

# Global activity log and its lock for thread safety
activity_log = []
_LOG_LOCK = threading.Lock()

# Maximum allowed number of entries to prevent uncontrolled resource consumption
_MAX_LOG_SIZE = 10_000

def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was logged, False if the log size limit prevented logging.
    """
    # Basic validation: reject empty uid or description
    if not uid or not description:
        return False

    # Prepare the log entry
    entry = {
        'uid': uid,
        'description': description,
        'timestamp': datetime.datetime.utcnow().isoformat() + "Z"
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not log to avoid uncontrolled growth
            return False
        activity_log.append(entry)
    return True