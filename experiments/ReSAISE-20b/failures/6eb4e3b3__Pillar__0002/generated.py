import threading
from typing import List, Tuple

# Global activity log and its lock to protect concurrent access.
activity_log: List[Tuple[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of records the log can hold before refusing new entries.
_MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was appended, False if the log size limit would be exceeded.
    """
    # Basic input validation to avoid accidental injection or malformed data
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Exceeded size limit; refuse to log more records.
            return False

        # Append the new record.  Using a tuple ensures immutability of the stored data.
        activity_log.append((uid, event))
        return True