from __future__ import annotations

import threading
from datetime import datetime
from typing import List, Tuple

# Global list that holds all activity logs.
# Each entry is a tuple: (timestamp, user_id, action)
activity_log: List[Tuple[str, str, str]] = []

# A lock to make the logging thread‑safe.
_log_lock = threading.Lock()


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a new activity entry to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the entry was added successfully, False otherwise.
    """
    # Basic validation to avoid corrupt data
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    timestamp = datetime.utcnow().isoformat()

    # Use a lock to prevent race conditions in multi‑threaded contexts.
    try:
        with _log_lock:
            activity_log.append((timestamp, user_id, action))
    except Exception:
        # In the unlikely event of a failure we return False.
        return False

    return True