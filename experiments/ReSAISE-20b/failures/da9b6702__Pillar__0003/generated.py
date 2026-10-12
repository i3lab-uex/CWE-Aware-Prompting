import threading
from datetime import datetime

# Global activity log and its configuration
activity_log = []
_activity_lock = threading.Lock()
_MAX_LOG_SIZE = 100_000          # Maximum number of entries allowed

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log
        exceeded its configured maximum size.
    """
    # Basic validation of input types to avoid accidental injection or malformed data
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        raise TypeError("Both user_identifier and task must be strings")

    # Prepare a structured record
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "action": task
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; do not append to avoid memory exhaustion
            return False

        activity_log.append(record)

    # Successful logging
    return True