import datetime
import threading

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed number of log entries
MAX_LOG_SIZE = 1000

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully,
        False if the log size limit would be exceeded.
    """
    # Basic input validation
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Trim whitespace to avoid accidental duplicates
    user_identifier = user_identifier.strip()
    task = task.strip()

    # Prepare the event record
    event_record = {
        "user": user_identifier,
        "task": task,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    with _activity_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(event_record)

    return True