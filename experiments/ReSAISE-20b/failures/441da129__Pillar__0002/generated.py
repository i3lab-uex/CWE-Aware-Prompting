import threading

# Global activity log and its maximum allowed size.
activity_log = []
MAX_LOG_SIZE = 10_000          # adjust as needed for your environment
_log_lock = threading.Lock()   # ensures thread‑safe writes


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the event was added, False if the log is full and the entry was rejected.
    """
    # Basic validation: ensure inputs are strings; silently ignore otherwise
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        return False

    # Acquire lock to protect concurrent modifications
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries once the maximum size is reached
            return False

        # Append a tuple (user_key, action_details) to the log
        activity_log.append((user_key, action_details))
    return True