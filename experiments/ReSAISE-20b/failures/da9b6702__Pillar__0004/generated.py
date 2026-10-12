import threading
from typing import List

# Global activity log and its lock for thread‑safety
activity_log: List[dict] = []
_activity_lock = threading.Lock()

# Maximum allowed entries in the log
_MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global activity_log.

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

    Notes
    -----
    * The function is thread‑safe.
    * Inputs are not modified to prevent side effects.
    * If the log exceeds _MAX_LOG_SIZE, the function refuses to add
      new entries rather than silently truncating or overwriting.
    """
    # Basic validation (prevent empty identifiers)
    if not user_identifier:
        return False

    record = {
        "user_id": user_identifier,
        "task": task,
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; refuse to add new record
            return False

        activity_log.append(record)
    return True