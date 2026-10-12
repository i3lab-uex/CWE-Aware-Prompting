import threading
from datetime import datetime

# Global list to store activity logs.
activity_log = []

# Configuration: maximum number of log entries allowed (to mitigate CWE‑770).
MAX_LOG_SIZE = 10_000

# Lock to ensure thread‑safe access to the log.
_log_lock = threading.Lock()


def _should_accept_new_entry() -> bool:
    """Check whether a new log entry can be added without exceeding the limit."""
    return len(activity_log) < MAX_LOG_SIZE


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a new activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was successfully logged, False otherwise.
    """
    # Basic input validation: ensure non‑empty strings to avoid accidental
    # injection of malformed data.
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False
    if not user_id.strip() or not action.strip():
        return False

    # Prepare the log entry.
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "action": action,
    }

    # Thread‑safe append with size check.
    with _log_lock:
        if not _should_accept_new_entry():
            # Log size limit reached; reject the new entry.
            return False
        activity_log.append(entry)

    return True