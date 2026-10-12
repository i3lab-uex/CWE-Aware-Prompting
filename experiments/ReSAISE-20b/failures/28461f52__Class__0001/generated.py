#!/usr/bin/env python3
"""
Activity log tracker with resource consumption control.

This module provides a thread‑safe function `track_user_event` that appends
user activity records to a global list while enforcing a maximum log size.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict, Any

# Global activity log and its maximum allowed size.
activity_log: List[Dict[str, Any]] = []
_MAX_LOG_SIZE: int = 10_000

# A lock to protect concurrent modifications of the log.
_log_lock = threading.Lock()


def _current_timestamp() -> str:
    """Return an ISO‑8601 formatted UTC timestamp."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        A unique identifier for the user who performed the action.
    event_description : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added,
        False if it was not added due to exceeding the maximum allowed size.

    Notes
    -----
    - The function is thread‑safe; it uses a lock to serialize access to the
      global `activity_log`.
    - The function enforces an upper bound on the number of log entries to
      mitigate CWE‑400: uncontrolled resource consumption.
    """
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        # Defensive programming: ensure inputs are strings.
        return False

    entry = {
        "timestamp": _current_timestamp(),
        "user_name": user_name,
        "event_description": event_description,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not append.
            return False
        activity_log.append(entry)

    return True


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     success = track_user_event("alice", "logged in")
#     print(f"Event logged: {success}")