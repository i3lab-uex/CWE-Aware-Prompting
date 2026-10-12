import threading

# Global activity log and its maximum allowed size.
activity_log = []
_LOG_MAX_SIZE = 10_000

# A lock to ensure thread‑safe updates to the global log.
_log_lock = threading.Lock()


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user who performed the action.
    act_description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log exceeded its size limit.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Construct a record. Using a tuple keeps the entry immutable.
    record = (uid, act_description)

    with _log_lock:
        if len(activity_log) >= _LOG_MAX_SIZE:
            # Do not add new entries once the limit is reached.
            return False
        activity_log.append(record)
    return True