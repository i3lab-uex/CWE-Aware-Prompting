import time
from threading import Lock

# Global activity log list and its maximum allowed size.
activity_log = []
_MAX_LOG_SIZE = 10_000          # adjust as appropriate for your environment
_log_lock = Lock()              # ensures thread‑safe modifications


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log is at its limit.
    """
    # Basic validation to avoid malformed entries
    if not uid or not act_description:
        return False

    # Build the log entry as a tuple (timestamp, uid, act_description)
    timestamp = time.time()
    entry = (timestamp, uid, act_description)

    with _log_lock:
        # Enforce a maximum size to mitigate uncontrolled resource consumption
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)
    return True