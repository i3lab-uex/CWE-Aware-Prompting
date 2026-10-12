import time
from threading import Lock

# Global activity log and configuration
activity_log: list[dict] = []
_MAX_LOG_SIZE = 1000            # maximum number of entries allowed
_log_lock = Lock()              # protects concurrent access to activity_log


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    act_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        ``True`` if the entry was added successfully, otherwise ``False``
        (e.g., when the log has reached its maximum size).

    Notes
    -----
    * The function is thread‑safe.
    * Input validation ensures both arguments are strings; otherwise a
      ``TypeError`` is raised.
    * The timestamp is recorded as seconds since the epoch in UTC.
    """
    # Basic type validation
    if not isinstance(uid, str):
        raise TypeError("uid must be a string")
    if not isinstance(act_description, str):
        raise TypeError("act_description must be a string")

    # Prepare the log entry
    entry = {
        "timestamp": time.time(),
        "uid": uid,
        "action": act_description
    }

    # Thread‑safe update of the log with size limit check
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(entry)
    return True