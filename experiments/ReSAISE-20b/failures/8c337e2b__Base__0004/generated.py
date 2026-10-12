import threading
from datetime import datetime

# Global log list and a lock for thread‑safety.
activity_log: list[dict[str, str]] = []
_LOG_LOCK = threading.Lock()

# Maximum number of log entries allowed (CWE‑770 mitigation).
_MAX_LOG_SIZE = 10_000


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging succeeded, False otherwise.
    """
    # Basic input validation to avoid malformed entries
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "action": action,
    }

    with _LOG_LOCK:
        # Enforce maximum log size to mitigate resource exhaustion
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Option 1: discard oldest entry (FIFO)
            activity_log.pop(0)

        try:
            activity_log.append(record)
        except Exception:  # pragma: no cover
            return False

    return True