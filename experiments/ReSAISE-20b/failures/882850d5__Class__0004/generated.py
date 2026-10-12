import time
from typing import List, Tuple

# Global activity log and its maximum allowed size.
activity_log: List[Tuple[str, str, float]] = []
MAX_LOG_SIZE: int = 10_000   # Adjust as needed for your environment.

# Optional lock for thread‑safety in multi‑threaded contexts.
try:
    from threading import Lock
    _log_lock = Lock()
except Exception:          # pragma: no cover
    _log_lock = None


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user.
    interaction_desc : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log has reached MAX_LOG_SIZE.
    """
    # Quick sanity check: skip empty entries to avoid bloating the log with meaningless data.
    if not user_alias or not interaction_desc:
        return False

    # Prepare the log entry: (user, description, timestamp)
    entry = (user_alias.strip(), interaction_desc.strip(), time.time())

    # Use a lock if available to avoid race conditions in concurrent environments.
    if _log_lock:
        with _log_lock:
            if len(activity_log) >= MAX_LOG_SIZE:
                return False
            activity_log.append(entry)
    else:
        # Single‑threaded fallback
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(entry)

    return True