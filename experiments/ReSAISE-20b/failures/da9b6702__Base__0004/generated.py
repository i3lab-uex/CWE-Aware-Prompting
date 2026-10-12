import threading
from datetime import datetime

# Global activity log and configuration
activity_log: list[dict] = []
LOG_MAX_SIZE = 10_000          # Maximum number of records allowed
log_lock = threading.Lock()    # Protect concurrent modifications


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log is at its maximum size.
    """
    # Basic validation to guard against malformed input
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "task": task,
    }

    with log_lock:
        if len(activity_log) >= LOG_MAX_SIZE:
            # Log is full; refuse to add more entries
            return False

        activity_log.append(record)
    return True