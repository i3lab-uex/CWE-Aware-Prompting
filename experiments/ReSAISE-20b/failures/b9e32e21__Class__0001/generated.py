import threading

# Global activity log and its configuration
MAX_LOG_ENTRIES = 10_000          # maximum number of entries allowed
activity_log: list[tuple[str, str]] = []  # each entry is (uid, act_description)
_log_lock = threading.Lock()      # protects concurrent modifications


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user who performed the action.
    act_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was added successfully.
        False if adding it would exceed MAX_LOG_ENTRIES and thus is rejected.

    Notes
    -----
    * The function uses a global lock to guard concurrent writes.
    * If the log size is already at or above MAX_LOG_ENTRIES, the function
      returns False without modifying the log to prevent uncontrolled growth.
    * The implementation is intentionally simple; for production use, a
      dedicated logging system or database would be preferable.
    """
    # Quick check to avoid acquiring the lock if we are definitely over limit
    if len(activity_log) >= MAX_LOG_ENTRIES:
        return False

    with _log_lock:
        # Re-check inside the lock to avoid race conditions
        if len(activity_log) >= MAX_LOG_ENTRIES:
            return False

        # Append the new record
        activity_log.append((uid, act_description))
    return True