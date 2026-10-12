#!/usr/bin/env python3
"""
Utility module for recording user interactions.

This module provides a thread‑safe function `save_user_interaction` that
appends a user action to the global activity log.  A hard limit on the number
of stored entries is enforced to prevent uncontrolled memory growth.
"""

import datetime
import threading
from typing import List

# Global activity log and configuration constants
activity_log: List[dict] = []          # Stores log entries as dictionaries.
MAX_LOG_ENTRIES: int = 10_000          # Maximum number of log entries allowed.
_log_lock = threading.Lock()           # Protects concurrent access to activity_log.

def _sanitize_input(value: str) -> str:
    """
    Basic sanitization to remove control characters that might interfere with
    log formatting or storage.  This is a minimal safeguard; callers should
    perform additional validation if needed.
    """
    return ''.join(ch for ch in value if 32 <= ord(ch) <= 126)

def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user performing the action.
    interaction_desc : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the entry was added successfully, False otherwise (e.g. when
        the log has reached its maximum size).

    Notes
    -----
    - The function is thread‑safe.
    - Inputs are sanitized to strip non‑printable characters.
    - No exceptions are raised; failures are indicated by a False return value.
    """
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        # Reject non‑string inputs silently.
        return False

    sanitized_alias = _sanitize_input(user_alias)
    sanitized_desc = _sanitize_input(interaction_desc)

    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + "Z",
        'user_alias': sanitized_alias,
        'interaction_desc': sanitized_desc
    }

    with _log_lock:
        if len(activity_log) >= MAX_LOG_ENTRIES:
            # Log is full; do not add new entry.
            return False
        activity_log.append(entry)

    return True