import threading
from datetime import datetime

# Global activity log and lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Optional limit on the number of log entries (adjust as needed)
_MAX_LOG_ENTRIES = 10_000


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Records a user action into the global activity_log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user performing the action.
    event_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was added; False if adding would exceed _MAX_LOG_ENTRIES.

    Notes
    -----
    * Thread‑safe via a global lock.
    * Each log entry is a dictionary containing the user, description,
      and timestamp in ISO 8601 format.
    * No exceptions are raised; the function silently returns False
      if the log size limit is reached.
    """
    # Basic input validation (prevent empty values)
    if not user_name or not event_description:
        return False

    # Construct the log entry
    entry = {
        "user": user_name,
        "event": event_description,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            return False
        activity_log.append(entry)
    return True