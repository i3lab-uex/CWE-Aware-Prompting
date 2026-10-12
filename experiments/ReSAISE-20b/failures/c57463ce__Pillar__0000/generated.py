import threading
from datetime import datetime

# Global activity log and its associated lock for thread‑safety.
activity_log: list[dict] = []
_log_lock = threading.Lock()

# Maximum allowed entries in the activity log. Adjust as needed.
MAX_LOG_SIZE = 100_000


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        ``True`` if the event was appended to the log, ``False`` if the
        operation was rejected because the log has reached its size limit.
    """
    # Basic input validation (prevent empty identifiers).
    if not uid or not description:
        return False

    # Prepare the log entry with a timestamp.
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    # Ensure that only one thread modifies the log at a time.
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries when the log is full.
            return False
        activity_log.append(entry)

    return True