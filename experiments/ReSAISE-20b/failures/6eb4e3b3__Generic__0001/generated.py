import datetime
from threading import Lock

# Global activity log and configuration
activity_log: list[tuple[str, str, datetime.datetime]] = []
MAX_LOG_SIZE: int = 100_000          # maximum number of entries allowed
_log_lock = Lock()                   # ensures thread‑safe updates


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was added, False if the log would exceed MAX_LOG_SIZE.
    """
    # Basic validation
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Create the log entry with a UTC timestamp
    entry = (uid, event, datetime.datetime.utcnow())

    # Thread‑safe append with size check
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(entry)

    return True