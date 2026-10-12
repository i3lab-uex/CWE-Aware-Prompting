#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Activity logger module.

This module provides a thread‑safe function `log_user_event` that records
user actions into a global activity log.  The log is capped at a maximum
size to prevent uncontrolled memory growth (CWE‑664: improper control of
a resource through its lifetime).
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict, Any

# Global activity log and its maximum size.
activity_log: List[Dict[str, Any]] = []
_MAX_LOG_SIZE = 10_000

# A re‑entrant lock to serialize access to the log.
_log_lock = threading.RLock()


def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Append a user event to the global activity log.

    Parameters
    ----------
    user_key : str
        A unique identifier for the user performing the action.
    action_details : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the event was recorded; False if the log has reached its
        configured maximum size.

    Notes
    -----
    * The function is thread‑safe: concurrent calls are serialized by a lock.
    * Events are stored as dictionaries containing the user key, action
      details, and a UTC timestamp.
    * No exceptions are raised; the function returns ``False`` when the log
      cannot accept new entries due to size limits.
    """
    # Basic validation: ensure inputs are strings.
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        # In a real system we might log this misuse; here we silently ignore.
        return False

    event: Dict[str, Any] = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_key": user_key,
        "action_details": action_details,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entries.
            return False

        activity_log.append(event)
        return True