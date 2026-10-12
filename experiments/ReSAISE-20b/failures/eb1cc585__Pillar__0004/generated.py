import time
from typing import List

# Global activity log list. In a real system this might be persisted to disk or a database.
activity_log: List[dict] = []

# Maximum number of entries the log is allowed to hold.
MAX_LOG_SIZE = 10_000

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Records a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        A unique string identifier associated with the user performing the action.
    event : str
        A textual description detailing the specific action undertaken by the user.

    Returns
    -------
    bool
        True if the activity was successfully logged, False if the logging attempt
        was rejected due to size limitations.
    """
    # Basic validation: ensure inputs are non-empty strings
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(event, str) or not event:
        return False

    # Enforce a maximum log size to avoid uncontrolled resource consumption
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a log entry with a timestamp for auditability
    entry = {
        "timestamp": time.time(),
        "user_identifier": user_identifier,
        "event": event,
    }

    # Append the entry to the global log
    activity_log.append(entry)
    return True