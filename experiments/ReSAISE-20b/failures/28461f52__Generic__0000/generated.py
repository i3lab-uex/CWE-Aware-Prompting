import threading
from datetime import datetime

# Global activity log and lock for thread safety
activity_log = []
_LOG_LOCK = threading.Lock()

# Optional maximum number of log entries (adjust as needed)
_MAX_LOG_SIZE = 10_000


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user.
    event_description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log is at capacity.

    Notes
    -----
    * The function is thread‑safe.
    * Each log entry contains a UTC timestamp, the user name and
      the event description.
    """
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        # Defensive check – silently ignore invalid input
        return False

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_name": user_name,
        "event_description": event_description,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(entry)

    return True