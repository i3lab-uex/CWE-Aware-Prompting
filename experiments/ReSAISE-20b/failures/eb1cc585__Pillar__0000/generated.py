import datetime
from typing import List, Dict
import threading

# Global activity log and its lock for thread‑safety.
activity_log: List[Dict[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log. Adjust as needed.
_MAX_LOG_SIZE = 10000


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the action was logged; False if the log is at capacity.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; failures are indicated by the return value.
    """
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        # Defensive check: silently ignore invalid types
        return False

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "event": event,
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject the new entry.
            return False
        activity_log.append(entry)

    return True