import threading

# Global activity log and its configuration
activity_log = []
MAX_LOG_SIZE = 10_000          # Maximum number of entries allowed in the log
_log_lock = threading.Lock()   # Ensure thread‑safe access to activity_log


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the entry was added successfully; False if the log is full.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        raise TypeError("user_identifier and event must be strings")

    # Enforce size limit to mitigate CWE‑770
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; reject new entries
            return False

        # Append a new record (timestamp can be added if needed)
        activity_log.append((user_identifier, event))
        return True