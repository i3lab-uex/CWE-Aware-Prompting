import datetime
import threading

# Global activity log list and its maximum allowed size.
activity_log: list[dict] = []
MAX_LOG_SIZE = 10_000          # Adjust as needed for your environment
_log_lock = threading.Lock()   # Ensure thread‑safe modifications


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_key : str
        Unique identifier of the user performing the action.
    action_details : str
        Human‑readable description of what was performed.

    Returns
    -------
    bool
        True if the event was added to the log.
        False if the log has reached its maximum size and the entry is discarded.

    Notes
    -----
    * The function protects against unlimited growth of ``activity_log`` by
      rejecting new entries once ``MAX_LOG_SIZE`` is reached.
    * Thread safety is guaranteed via a module‑level lock.
    """
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Reject new entries to avoid unbounded memory consumption
            return False

        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user_key": user_key,
            "action_details": action_details,
        }
        activity_log.append(entry)
    return True