import datetime
import threading

# Global activity log list and a lock for thread‑safety.
activity_log = []
_LOG_LOCK = threading.Lock()

# Maximum number of entries the log can hold. Adjust as needed.
_MAX_LOG_SIZE = 10_000


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user event in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the event was logged, False if the log is full.

    Notes
    -----
    - The function is thread‑safe.
    - If the log reaches its maximum size, new entries are rejected
      to prevent uncontrolled resource consumption (CWE‑400).
    """
    # Basic input validation – avoid None or empty values.
    if not uid or not description:
        return False

    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "description": description,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries when the log is full.
            return False
        activity_log.append(event)

    return True