import threading
from datetime import datetime

# Global activity log and configuration constants
activity_log = []
MAX_LOG_SIZE = 10_000            # maximum number of entries to keep
LOG_LOCK = threading.Lock()      # protects concurrent access

def track_user_event(uid: str, description: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the event was added to the log, False if the
        operation failed due to size limitations.
    """
    # Basic validation – reject empty values early
    if not uid or not description:
        return False

    # Build the log entry with a timestamp
    entry = {
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "uid": uid,
        "description": description
    }

    with LOG_LOCK:
        # Enforce size limit – reject new entries if the log is full
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        activity_log.append(entry)

    return True