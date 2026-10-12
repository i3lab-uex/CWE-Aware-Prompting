import time
from threading import Lock

# Global activity log and lock for thread‑safety
activity_log: list[dict] = []
_log_lock = Lock()

# Maximum number of entries allowed in the log
MAX_LOG_SIZE: int = 100_000

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the action was recorded, False if the log size limit prevented it.
    """
    # Basic validation to avoid storing empty or malicious entries
    if not user_identifier or not event:
        return False

    # Prepare the record with a timestamp
    record = {
        "user_id": user_identifier,
        "event": event,
        "timestamp": time.time(),
    }

    with _log_lock:
        # Enforce maximum log size
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(record)

    return True