import threading
from typing import List

# Global activity log and associated lock for thread‑safety
activity_log: List[dict] = []
_log_lock = threading.Lock()

# Maximum number of entries the log is allowed to hold
MAX_LOG_SIZE: int = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was added successfully,
        False if the log has reached its maximum size.
    """
    # Basic type checking to avoid accidental misuse
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Prepare the record
    record = {
        "uid": uid,
        "event": event,
    }

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log size limit reached – reject new entry
            return False

        activity_log.append(record)
    return True