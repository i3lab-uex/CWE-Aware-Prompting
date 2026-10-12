import threading
from datetime import datetime

# Global activity log and lock for thread safety
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()

# Maximum number of records allowed in the log
_MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was successfully added, False if the log has reached its maximum size.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Construct the record
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "event": event,
    }

    # Use a lock to ensure atomic check-and-insert
    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(record)

    return True