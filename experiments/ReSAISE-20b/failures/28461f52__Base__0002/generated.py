import threading
from datetime import datetime

# Global activity log and lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries to prevent unbounded growth (CWE-770 mitigation)
_MAX_LOG_SIZE = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Identifier for the user who performed the action.
    event_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if adding it would exceed the configured limit.
    """
    # Basic validation to avoid storing empty entries
    if not user_name or not event_description:
        return False

    # Create a log entry with timestamp
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_name": user_name,
        "event_description": event_description
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not add the entry and signal failure
            return False

        activity_log.append(entry)
        return True