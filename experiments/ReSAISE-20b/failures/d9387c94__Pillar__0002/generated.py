import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries the log can hold
_MAX_LOG_SIZE = 10_000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    account : str
        Unique identifier of the user performing the action.
    operation : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was successfully appended,
        False if appending would exceed the maximum log size.
    """
    # Basic input validation
    if not isinstance(account, str) or not isinstance(operation, str):
        return False

    # Prepare the record with a timestamp
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "account": account,
        "operation": operation,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not exceed the size limit
            return False

        activity_log.append(record)
        return True