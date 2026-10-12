import threading

# Global activity log and a lock for thread‑safe updates
activity_log: list[dict[str, str]] = []
_log_lock = threading.Lock()

# Maximum number of log entries allowed to prevent unbounded growth
_MAX_LOG_SIZE = 10_000

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
        True if the entry was added, False if the log size limit was reached.

    Notes
    -----
    - Thread‑safe: uses a lock to serialize access.
    - Enforces an upper bound on the log size to mitigate CWE‑770.
    """
    if not isinstance(uid, str) or not isinstance(act_description, str):
        raise TypeError("uid and act_description must be strings")

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; do not add new entry
            return False

        activity_log.append({
            "uid": uid,
            "action": act_description
        })
    return True