import threading

# Global activity log and a lock to ensure thread‑safety.
activity_log: list[tuple[str, str]] = []
_LOG_LOCK = threading.Lock()

# Maximum number of entries allowed in the log to avoid uncontrolled growth.
_MAX_LOG_SIZE = 10_000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    account : str
        Unique identifier of the user performing the action.
    operation : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the record was added successfully, False if adding would exceed
        _MAX_LOG_SIZE.
    """
    # Basic validation to prevent empty or malformed entries.
    if not account or not operation:
        return False

    # Use a lock to avoid race conditions in multi‑threaded environments.
    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not append to prevent uncontrolled growth.
            return False

        activity_log.append((account, operation))
    return True