import threading
from typing import List, Tuple

# Global activity log and a lock for thread‑safety.
_activity_log_lock = threading.Lock()
# Use a deque with a maximum length to prevent uncontrolled growth (CWE‑400).
from collections import deque
activity_log: List[Tuple[str, str]] = list()
MAX_LOG_SIZE = 10_000   # Adjust as appropriate for the system

def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the entry was logged successfully, False otherwise.
    """
    # Basic validation to avoid corrupt entries
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    # Ensure that the log does not grow unbounded.
    with _activity_log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Remove the oldest entry to make room.
            activity_log.pop(0)
        try:
            activity_log.append((user_id, action))
            return True
        except Exception:
            # In the unlikely event of an append failure, do not crash.
            return False