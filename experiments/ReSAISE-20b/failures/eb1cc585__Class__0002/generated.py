import time
from threading import Lock

# Global activity log and a lock to make the operation thread‑safe.
activity_log = []
_activity_lock = Lock()

# Maximum number of entries allowed in the log. Adjust as needed.
_MAX_LOG_SIZE = 10_000

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Append a user action to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Textual description of the event.

    Returns
    -------
    bool
        True if the entry was added, False if the log is at its maximum size.
    """
    # Basic validation to avoid accidental injection of malicious data
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Truncate overly long strings to avoid excessive memory usage
    user_identifier = user_identifier[:256]
    event = event[:1024]

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full – reject the new entry
            return False

        activity_log.append({
            "user": user_identifier,
            "event": event,
            "timestamp": time.time()
        })
    return True