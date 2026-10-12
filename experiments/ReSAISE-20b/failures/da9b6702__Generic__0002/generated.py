import threading
from datetime import datetime

# Global activity log and lock for thread‑safety
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()
_MAX_LOG_SIZE = 10_000  # maximum number of records allowed


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the event was logged, False if the log size limit would be exceeded.
    """
    # Basic validation to guard against injection or accidental misuse
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Truncate excessively long strings to prevent log bloat
    user_identifier = user_identifier[:256]
    task = task[:1024]

    event_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_identifier": user_identifier,
        "task": task,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log limit reached; refuse to add new entry
            return False

        activity_log.append(event_record)

    return True