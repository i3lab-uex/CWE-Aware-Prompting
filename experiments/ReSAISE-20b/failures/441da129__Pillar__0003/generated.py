import threading
from datetime import datetime

# Global activity log and associated lock for thread safety.
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of entries the log can hold.  Adjust as needed.
_MAX_LOG_SIZE = 100_000

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Register a user action in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Human‑readable description of the action performed.

    Returns
    -------
    bool
        True if the event was appended to the log, False if the log is at capacity.

    Notes
    -----
    - The function is thread‑safe and protects the global log with a lock.
    - No exception is raised; if an error occurs internally it will be swallowed
      and False returned.
    """
    try:
        with _activity_lock:
            if len(activity_log) >= _MAX_LOG_SIZE:
                # Reject new entries when the log reaches its maximum size.
                return False
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "user_key": user_key,
                "action_details": action_details,
            }
            activity_log.append(entry)
        return True
    except Exception:
        # Swallow unexpected errors to avoid leaking internal state.
        return False