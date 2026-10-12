import time
from typing import List, Dict
import threading

# Global activity log and its lock for thread‑safe access
activity_log: List[Dict[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of records allowed in the log
_MAX_LOG_SIZE = 1000


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
        True if the event was logged successfully, False if the log size limit would be exceeded.
    """
    # Construct a record with a timestamp
    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
        "user_id": user_identifier,
        "task": task,
    }

    # Use a lock to avoid race conditions in concurrent environments
    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not append; return False to signal failure
            return False

        activity_log.append(record)
    return True