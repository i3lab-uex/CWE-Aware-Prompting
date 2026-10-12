import threading

# Global activity log and its lock for thread safety
activity_log = []
_activity_lock = threading.Lock()

# Maximum allowed entries in the activity log to avoid resource exhaustion
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity log.

    Args:
        uid (str): Unique identifier for the user.
        event (str): Description of the action performed.

    Returns:
        bool: True if the record was added successfully, False if the log
              has reached its maximum size and the action could not be logged.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log has reached its capacity; refuse to add more entries
            return False

        activity_log.append({'uid': uid, 'event': event})
        return True