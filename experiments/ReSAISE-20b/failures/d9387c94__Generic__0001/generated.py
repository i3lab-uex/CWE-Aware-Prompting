import threading
from datetime import datetime

# Global activity log and its configuration
activity_log: list[dict] = []
_MAX_LOG_SIZE = 10_000          # Maximum number of records allowed
_log_lock = threading.Lock()    # Protects concurrent access to the log


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the operation.
    operation : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was appended successfully.
        False if the log is already at its maximum size.

    Notes
    -----
    - Input values are coerced to strings to avoid type errors.
    - A timestamp in ISO 8601 format (UTC) is added automatically.
    - Thread safety is ensured via a lock to prevent race conditions
      when multiple threads attempt to log simultaneously.
    """
    # Coerce inputs to strings (basic sanitization)
    account_str = str(account)
    operation_str = str(operation)

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "account": account_str,
        "operation": operation_str,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(record)

    return True