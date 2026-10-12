import threading

# Global activity log and its lock for thread‑safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of records allowed in the log to avoid uncontrolled growth
_MAX_LOG_SIZE = 10_000

def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was successfully appended, False if the log has reached its maximum size.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(account, str) or not isinstance(operation, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; reject new entries
            return False

        # Record structure: (account, operation)
        activity_log.append((account, operation))
    return True