import datetime
import threading

# Global activity log and its configuration
activity_log = []
_activity_lock = threading.Lock()
_MAX_LOG_SIZE = 10_000   # maximum number of entries allowed


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Register a user event in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully,
        False if the log has reached its maximum capacity.
    """
    # Basic validation
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        raise TypeError("user_key and action_details must be strings")

    # Construct the log entry
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    entry = {
        "timestamp": timestamp,
        "user_key": user_key,
        "action_details": action_details
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Reject new entries once the limit is reached
            return False

        activity_log.append(entry)
    return True