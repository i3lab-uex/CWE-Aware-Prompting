import threading

# Global activity log and configuration
MAX_LOG_SIZE = 10_000          # maximum number of entries to keep in memory
activity_log: list[tuple[str, str]] = []  # each entry is (user_id, action)
_log_lock = threading.Lock()   # ensures thread‑safe updates

def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the entry was successfully appended, False otherwise.
    """
    # Basic validation: ensure non‑empty strings
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(action, str) or not action:
        return False

    with _log_lock:
        # Enforce a maximum size to mitigate CWE‑770
        if len(activity_log) >= MAX_LOG_SIZE:
            # Remove the oldest entry to make room
            activity_log.pop(0)

        try:
            activity_log.append((user_id, action))
        except Exception:  # pragma: no cover
            return False

    return True