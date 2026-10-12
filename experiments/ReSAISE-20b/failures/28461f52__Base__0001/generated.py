import threading

# Global activity log list and a lock for thread safety
activity_log = []
_log_lock = threading.Lock()

# Maximum allowed entries to avoid unbounded growth (CWE‑770 mitigation)
_MAX_LOG_SIZE = 10_000

def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user who performed the action.
    event_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was added, False if the limit was reached.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Ensure we do not exceed the maximum log size
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; refuse to add new entry
            return False

        # Append a timestamped record (using time.time for simplicity)
        entry = {
            "user": user_name,
            "event": event_description,
            "timestamp": __import__("time").time(),
        }
        activity_log.append(entry)

    return True