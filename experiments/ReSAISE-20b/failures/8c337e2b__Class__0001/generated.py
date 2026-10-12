# log_user_activity.py

from datetime import datetime
from threading import Lock

# Global activity log (list of dicts). In a real application, consider persisting to a database.
activity_log: list[dict] = []

# Maximum number of entries to keep in memory. Older entries will be discarded when the limit is exceeded.
_MAX_LOG_ENTRIES = 10_000

# Lock to make logging thread‑safe in a multi‑threaded environment.
_log_lock = Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the log entry was added successfully, False otherwise.

    Notes
    -----
    * The function is thread‑safe.
    * To mitigate CWE-400 (Uncontrolled Resource Consumption) a maximum number of
      log entries is enforced. When the limit is reached, the oldest entry is removed.
    * If either argument is not a string or empty, the function returns False
      without modifying the log.
    """
    # Basic validation: ensure both arguments are non-empty strings
    if not isinstance(user_id, str) or not user_id.strip():
        return False
    if not isinstance(action, str) or not action.strip():
        return False

    # Construct the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "action": action,
    }

    with _log_lock:
        # Maintain the size limit
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Remove the oldest entry (index 0)
            activity_log.pop(0)

        activity_log.append(entry)

    return True