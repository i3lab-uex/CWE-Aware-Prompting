import threading
from datetime import datetime

# Global activity log and its maximum allowed size
activity_log = []
_activity_lock = threading.Lock()
_MAX_LOG_SIZE = 10_000   # adjust as needed

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a new user activity record to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully,
        False if the log has reached its maximum size.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not add new record
            return False

        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_identifier,
            "task": task
        }
        activity_log.append(event)
    return True