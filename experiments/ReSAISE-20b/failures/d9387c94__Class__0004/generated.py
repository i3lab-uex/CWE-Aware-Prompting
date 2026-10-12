import threading

# Global activity log (list of tuples: (account, operation))
activity_log = []

# Maximum number of entries allowed in the log
MAX_LOG_SIZE = 1000

# Lock to ensure thread‑safe updates to the activity log
_log_lock = threading.Lock()


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
        False if appending would exceed `MAX_LOG_SIZE`.
    """
    # Basic validation (avoid storing empty strings)
    if not account or not operation:
        return False

    with _log_lock:
        # Check against the maximum size to prevent uncontrolled resource consumption
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        # Append the new record
        activity_log.append((account, operation))
        return True