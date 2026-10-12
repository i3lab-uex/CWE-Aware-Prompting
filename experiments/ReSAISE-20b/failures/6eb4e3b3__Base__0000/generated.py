import datetime
from typing import List, Tuple

# Global activity log (in-memory). In a real system this would be persisted to disk or a database.
activity_log: List[Tuple[str, str, datetime.datetime]] = []

# Maximum number of records allowed in the log to prevent unbounded memory usage (CWE-770 mitigation).
MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Args:
        uid (str): Unique identifier of the user performing the action.
        event (str): Description of the specific action taken.

    Returns:
        bool: True if the record was successfully added, False if adding would exceed MAX_LOG_SIZE.
    """
    global activity_log

    # Enforce log size limit to avoid unlimited memory growth
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Record the current timestamp
    timestamp = datetime.datetime.utcnow()

    # Append a tuple (uid, event, timestamp) to the log
    activity_log.append((uid, event, timestamp))
    return True