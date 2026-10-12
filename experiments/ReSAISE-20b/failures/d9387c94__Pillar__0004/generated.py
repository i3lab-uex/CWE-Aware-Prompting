import threading

# Global activity log and a lock for thread‑safety
activity_log: list[tuple[str, str]] = []
_log_lock = threading.Lock()

# Maximum number of records allowed in the log
_MAX_LOG_SIZE: int = 10_000


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
        ``True`` if the record was added successfully,
        ``False`` if the log has reached its maximum size and
        therefore cannot accept new entries.

    Notes
    -----
    - The function is thread‑safe; a lock protects concurrent writes.
    - No exceptions are raised – failures due to size limits simply
      return ``False``.
    """
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; cannot record new activity.
            return False

        # Append a tuple (account, operation) to the log
        activity_log.append((account, operation))
        return True