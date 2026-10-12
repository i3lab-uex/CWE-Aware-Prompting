import threading
from typing import List

# Global activity log and configuration
activity_log: List[str] = []
_LOG_LOCK = threading.Lock()
_MAX_LOG_SIZE = 10_000  # Maximum number of entries allowed in the log


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global activity_log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging was successful, False otherwise (e.g., log size exceeded).
    """
    # Basic input validation
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    # Construct the log entry
    entry = f"{user_id}:{action}"

    with _LOG_LOCK:
        # Prevent uncontrolled growth of the log
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)

    return True