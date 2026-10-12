import threading

# Global activity log and its lock for thread‑safe updates
activity_log = []
_activity_lock = threading.Lock()

# Maximum number of log entries allowed (CWE‑770 mitigation)
_MAX_LOG_SIZE = 10_000

def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log is full.
    """
    # Basic input validation
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Prepare the log entry
    entry = {
        "uid": uid,
        "action": act_description,
        # Store a timestamp for auditing purposes
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    with _activity_lock:
        # Check for log size limit
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False

        activity_log.append(entry)

    return True