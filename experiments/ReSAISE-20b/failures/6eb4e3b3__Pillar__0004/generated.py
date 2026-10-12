#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Activity logging module.

This module defines a thread‑safe function `record_user_action` that appends
user activity records to a global in‑memory log while respecting a maximum size
constraint. The implementation mitigates CWE‑664 by ensuring that the resource
(the activity log) is correctly managed and released, even in multi‑threaded
contexts.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Tuple

# Global activity log and its configuration ---------------------------------

# Maximum number of records allowed in the log. Adjust as needed.
_MAX_LOG_SIZE: int = 10_000

# The in‑memory activity log. Each entry is a tuple:
# (timestamp: str, uid: str, event: str)
activity_log: List[Tuple[str, str, str]] = []

# A lock to protect concurrent access to `activity_log`.
_log_lock: threading.Lock = threading.Lock()


def _sanitize_string(value: str) -> str:
    """
    Perform minimal sanitization to avoid injection attacks or
    unintended control characters in the log.

    Parameters:
        value (str): The string to sanitize.

    Returns:
        str: A sanitized version of the input.
    """
    # Replace newline and carriage return to keep log entries on a single line.
    return value.replace("\n", " ").replace("\r", " ").strip()


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity log.

    The function is thread‑safe and respects the maximum log size.
    If adding a new record would exceed `_MAX_LOG_SIZE`, the function
    returns False and does not modify the log.

    Parameters:
        uid (str): Unique identifier of the user.
        event (str): Description of the action performed.

    Returns:
        bool: True if the record was logged successfully,
              False if the log size limit would be exceeded.
    """
    # Basic type checks (no exception is raised on failure).
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Sanitize inputs to avoid problematic characters.
    uid_clean = _sanitize_string(uid)
    event_clean = _sanitize_string(event)

    # Prepare the record with an ISO 8601 timestamp.
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    record: Tuple[str, str, str] = (timestamp, uid_clean, event_clean)

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; do not add the record.
            return False
        activity_log.append(record)

    return True