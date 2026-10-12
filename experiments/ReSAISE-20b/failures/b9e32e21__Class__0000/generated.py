import threading

# Global activity log and its maximum size limit
activity_log = []
MAX_LOG_SIZE = 10_000  # adjust as needed to avoid uncontrolled resource consumption
_log_lock = threading.Lock()


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action into the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Enforce log size limit to mitigate CWE-400
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append({"uid": uid, "action": act_description})
    return True