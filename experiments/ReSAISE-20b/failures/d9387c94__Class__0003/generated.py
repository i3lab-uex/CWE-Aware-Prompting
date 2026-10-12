import threading
from datetime import datetime

# Global activity log and its lock for thread safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of records allowed in the log to prevent uncontrolled resource consumption.
_MAX_LOG_SIZE = 10_000

def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    account : str
        Unique identifier of the user performing the action.
    operation : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was appended successfully,
        False if the log has reached its maximum size.
    """
    # Quick reject if we already hit the limit to avoid unnecessary locking overhead
    if len(activity_log) >= _MAX_LOG_SIZE:
        return False

    # Construct the record with a timestamp
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "account": account,
        "operation": operation
    }

    # Append to the log in a thread‑safe manner
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Double‑check after acquiring the lock
            return False
        activity_log.append(record)
    return True