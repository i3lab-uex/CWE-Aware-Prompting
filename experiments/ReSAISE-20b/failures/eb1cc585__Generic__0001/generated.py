import threading

# Global activity log and its configuration
activity_log = []          # List that stores all user action records
MAX_LOG_SIZE = 100_000     # Maximum number of entries allowed in the log

# Thread‑safety lock to guard concurrent modifications
_log_lock = threading.Lock()


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Records a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user performing the action.
    event : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the record was appended to ``activity_log``; False if the log has reached its
        configured maximum size and the record was rejected.
    """
    # Basic validation to avoid storing malformed entries
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Prepare the log entry (timestamp can be added if needed)
    entry = {
        "user": user_identifier,
        "event": event
    }

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries when the log is full
            return False

        activity_log.append(entry)
        return True