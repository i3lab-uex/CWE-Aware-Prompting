import threading

# Global activity log and a lock for thread‑safety
activity_log: list[dict[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log
_MAX_LOG_ENTRIES: int = 10_000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if it was rejected due to log size limits.
    """
    # Basic validation (ensure non-empty strings)
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(act_description, str) or not act_description:
        return False

    # Prepare the entry
    entry = {"uid": uid, "action": act_description}

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Log has reached its capacity; reject new entries
            return False

        activity_log.append(entry)
        return True