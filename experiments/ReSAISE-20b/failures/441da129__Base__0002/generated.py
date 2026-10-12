import threading
from datetime import datetime

# Global activity log and a lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed to prevent uncontrolled growth
_MAX_LOG_SIZE = 10_000

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
        True if the event was logged, False if the log is full.

    Notes
    -----
    - The function enforces a hard limit on the size of `activity_log`
      to mitigate CWE-770 (resource exhaustion).
    - Thread safety is ensured via a lock.
    """
    # Basic validation of inputs
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        raise TypeError("user_key and action_details must be strings")

    # Prepare the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "user_key": user_key,
        "action_details": action_details
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject the new entry
            return False

        activity_log.append(entry)
        return True