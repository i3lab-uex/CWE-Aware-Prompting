import threading
from typing import List, Tuple

# Global activity log and configuration limits
activity_log: List[Tuple[str, str]] = []
MAX_LOG_SIZE: int = 10_000          # Maximum number of entries allowed
LOG_LOCK = threading.Lock()         # Protects concurrent access to the log

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the activity was successfully logged,
        False if adding it would exceed MAX_LOG_SIZE.
    """
    # Basic validation to avoid malformed entries
    if not uid or not event:
        return False

    with LOG_LOCK:
        # Enforce the size limit to mitigate CWE-770
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        activity_log.append((uid, event))
    return True