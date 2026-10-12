#!/usr/bin/env python3
"""
Activity logging module.

Provides a thread‑safe helper `record_user_action` that appends user actions
to a global activity log while enforcing an optional maximum size.
"""

import datetime
import threading

# Global storage for activity records
activity_log: list[dict] = []

# Configuration: maximum number of log entries allowed.
MAX_LOG_SIZE = 10_000

# Thread‑safety lock for concurrent writes
_log_lock = threading.RLock()


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user performing the action.
    act_description : str
        Human‑readable description of the performed action.

    Returns
    -------
    bool
        ``True`` if the entry was added, ``False`` if it was rejected due to
        exceeding :data:`MAX_LOG_SIZE`.

    Notes
    -----
    * The function is thread‑safe; concurrent calls are serialized via a re‑entrant
      lock.
    * The log entry contains the timestamp in UTC ISO format, user id,
      and action description.
    * No exception is raised on failure; the caller should inspect the return
      value if needed.
    """
    # Basic validation (ensuring non‑empty strings)
    if not isinstance(uid, str) or not uid.strip():
        return False
    if not isinstance(act_description, str) or not act_description.strip():
        return False

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Exceeded maximum allowed entries; reject new log
            return False

        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user_id": uid,
            "action": act_description.strip(),
        }
        activity_log.append(entry)
    return True