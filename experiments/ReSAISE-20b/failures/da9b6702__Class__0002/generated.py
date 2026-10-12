import datetime
import threading

# Global activity log and its associated lock for thread safety.
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()

# Maximum allowed number of entries in the activity log to prevent uncontrolled resource consumption.
_MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user performing the action.
    task : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log size limit has been reached.
    """
    # Basic type validation to avoid accidental misuse.
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Build the event record with a timestamp.
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "task": task,
    }

    # Safely append to the log while enforcing size limits.
    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not append.
            return False
        activity_log.append(event)

    return True