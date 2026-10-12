import threading
from datetime import datetime

# Global activity log and a lock for thread‑safety.
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()

# Maximum number of log entries allowed to mitigate CWE‑400.
_MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Append a user action to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    act_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    # Basic validation
    if not uid or not act_description:
        return False

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "action": act_description,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; refuse to add more entries.
            return False
        activity_log.append(entry)
    return True