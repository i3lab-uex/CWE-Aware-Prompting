import threading
from datetime import datetime

# Global activity log and its maximum allowed size.
activity_log: list[dict] = []
_MAX_LOG_SIZE = 10_000          # Adjust as appropriate for your environment.
_log_lock = threading.Lock()    # Protects concurrent modifications to the log.

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user performing the action.
    task : str
        A description of the action taken by the user.

    Returns
    -------
    bool
        True if the event was successfully logged; False if the log has reached its maximum size.
    """
    # Basic validation to avoid malformed entries
    if not user_identifier or not task:
        return False

    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "task": task,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not grow beyond the limit to mitigate CWE‑770.
            return False
        activity_log.append(event)

    return True