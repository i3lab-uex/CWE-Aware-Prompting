import threading
from datetime import datetime

# Global activity log and its lock for thread‑safety.
activity_log: list[dict] = []
_activity_lock = threading.Lock()

# Maximum number of records allowed in the log.
_MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user event to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user.
    task : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log size limit was exceeded.

    Notes
    -----
    - The function is thread‑safe.
    - It does not raise exceptions; it simply returns False on failure.
    """
    # Basic validation to avoid injection-like issues
    if not isinstance(user_identifier, str) or not isinstance(task, str):
        return False

    # Truncate overly long strings to prevent abuse
    user_identifier = user_identifier[:256]
    task = task[:1024]

    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_identifier": user_identifier,
        "task": task,
    }

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not append.
            return False
        activity_log.append(event)

    return True