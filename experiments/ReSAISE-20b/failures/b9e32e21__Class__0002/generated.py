import threading
from datetime import datetime

# Global activity log and a lock for thread‑safety
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()
_MAX_LOG_SIZE = 10_000  # configurable limit to prevent uncontrolled growth


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    act_description : str
        Human‑readable description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log is at capacity.
    """
    # Validate inputs (basic type check)
    if not isinstance(uid, str) or not isinstance(act_description, str):
        raise TypeError("uid and act_description must be strings")

    # Prepare the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "action": act_description,
    }

    with _LOG_LOCK:
        # Enforce the maximum log size to avoid uncontrolled resource consumption
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)
    return True