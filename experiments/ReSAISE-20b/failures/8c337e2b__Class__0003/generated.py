# -*- coding: utf-8 -*-

"""
User activity logger.

This module provides a simple in‑memory logging facility that appends
user actions to a global list.  To mitigate uncontrolled resource
consumption (CWE‑400) the log is capped at a configurable maximum size.
When the limit is reached, the oldest entries are discarded (a simple
FIFO policy).
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Maximum number of entries to keep in the log.
MAX_LOG_SIZE: int = 10_000

# --------------------------------------------------------------------------- #
# Global state
# --------------------------------------------------------------------------- #

# The activity log itself – a list of tuples.
activity_log: List[Tuple[str, str, datetime.datetime]] = []

# A lock to make the logger thread‑safe.
_log_lock = threading.Lock()


def _trim_log_if_needed() -> None:
    """
    Remove oldest entries if the log exceeds MAX_LOG_SIZE.
    This prevents unbounded growth of the in‑memory list.
    """
    global activity_log
    if len(activity_log) > MAX_LOG_SIZE:
        # Remove the oldest entries to bring the size back within limits.
        excess = len(activity_log) - MAX_LOG_SIZE
        activity_log = activity_log[excess:]


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        ``True`` if the entry was added successfully, otherwise ``False``.

    Notes
    -----
    - The function is thread‑safe.
    - If the log exceeds ``MAX_LOG_SIZE`` the oldest entries are discarded
      to keep memory usage bounded.
    - The function never raises an exception; failures are reported via
      the boolean return value.
    """
    try:
        # Validate inputs – reject empty or non‑string values.
        if not isinstance(user_id, str) or not isinstance(action, str):
            return False
        if not user_id.strip() or not action.strip():
            return False

        # Prepare the log entry with a timestamp.
        timestamp = datetime.datetime.utcnow()

        with _log_lock:
            activity_log.append((user_id, action, timestamp))
            _trim_log_if_needed()

        return True
    except Exception:
        # In a real application you might log the exception to an error log.
        return False