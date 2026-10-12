import threading

# Global activity log and its maximum allowed size
activity_log: list[tuple[str, str]] = []
MAX_LOG_SIZE: int = 10_000

# A lock to make the function thread‑safe
_log_lock = threading.Lock()


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the record was appended, False if the log is already at its
        maximum size.

    Notes
    -----
    - The function uses a lock to prevent race conditions when accessed from
      multiple threads.
    - No exceptions are raised; failures due to size limits simply return False.
    """
    # Validate inputs (basic type check)
    if not isinstance(account, str) or not isinstance(operation, str):
        return False

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; cannot record more entries
            return False

        activity_log.append((account, operation))
        return True