#!/usr/bin/env python3
"""
User activity logger.

The module keeps a global in‑memory list `activity_log` that stores
records of user actions.  To avoid unbounded memory growth (CWE‑770),
the list is capped at a maximum number of entries (`MAX_LOG_SIZE`).
When the limit would be exceeded, the new event is rejected and
the function returns ``False``.  A simple thread‑safe lock protects the
log from concurrent modifications.

No exceptions are raised; failures are signalled via a boolean return value.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict

# Public API ---------------------------------------------------------------

def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a new user event to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action performed.

    Returns
    -------
    bool
        ``True`` if the event was logged successfully, ``False`` if adding
        it would exceed :data:`MAX_LOG_SIZE`.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; callers should check the return value.
    """
    global activity_log

    # Reject empty identifiers or tasks to avoid meaningless entries
    if not user_identifier or not task:
        return False

    # Create the event record
    record: Dict[str, str] = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "task": task,
    }

    # Acquire lock to ensure atomicity
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            return False
        activity_log.append(record)
    return True

# -------------------------------------------------------------------------

# Internal constants and state ---------------------------------------------

MAX_LOG_SIZE: int = 10_000   # Maximum number of entries in the log

# Global activity log – initially empty
activity_log: List[Dict[str, str]] = []

# Lock to protect concurrent access to the log
_log_lock = threading.Lock()