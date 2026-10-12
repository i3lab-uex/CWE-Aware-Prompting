#!/usr/bin/env python3
"""
User interaction logging module.

The `save_user_interaction` function records a user action in the global
`activity_log`.  It enforces a maximum number of stored entries to avoid
unbounded memory growth (CWE‑664: Improper Control of a Resource Through its Lifetime).
"""

from __future__ import annotations

import threading
from datetime import datetime
from typing import List, Tuple

# Global activity log and its associated lock.
activity_log: List[Tuple[str, str, datetime]] = []
_LOG_LOCK = threading.Lock()

# Maximum number of entries the log can hold.
_MAX_LOG_ENTRIES: int = 10_000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        A unique identifier for the user performing the action.
    interaction_desc : str
        A textual description of the user's action.

    Returns
    -------
    bool
        True if the log entry was added successfully, False if the log is full.

    Notes
    -----
    - The function uses a thread‑safety lock to prevent race conditions.
    - If the log has reached its maximum size, no new entry is added and
      False is returned.  Existing entries are left untouched.
    """
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        # Defensive check: reject non‑string inputs silently.
        return False

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            return False
        # Append a tuple of (alias, description, timestamp).
        activity_log.append((user_alias, interaction_desc, datetime.utcnow()))
    return True