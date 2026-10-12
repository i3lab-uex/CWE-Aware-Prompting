import threading

# Global activity log storage
activity_log = []
# Maximum allowed entries in the log (CWE-770 mitigation)
_MAX_LOG_SIZE = 10_000

# Lock to ensure thread‑safe modifications
_log_lock = threading.Lock()


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user who performed the action.
    act_description : str
        Textual description of the action taken.

    Returns
    -------
    bool
        True if the log entry was added, False if the log has reached its maximum size.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log has reached its maximum capacity; refuse to add more entries
            return False

        # Append the new record (timestamp could be added if needed)
        activity_log.append({
            "uid": uid,
            "action": act_description
        })
    return True