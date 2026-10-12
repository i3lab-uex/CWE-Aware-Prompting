#!/usr/bin/env python3
"""
Activity logging module.

This module provides a thread‑safe helper to record user interactions in an
in‑memory activity log.  The log is stored as a global list of dictionaries,
each containing the user alias, interaction description and a UTC timestamp.

The module enforces an upper bound on the number of stored log entries.
When that limit is reached, new entries are rejected and `False` is returned.

The implementation intentionally avoids raising exceptions on failure
and does not perform any external I/O to keep the function lightweight.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

MAX_LOG_SIZE: int = 10_000  # Maximum number of entries to keep in memory.

# --------------------------------------------------------------------------- #
# Global state
# --------------------------------------------------------------------------- #

activity_log: List[Dict[str, str]] = []
_log_lock = threading.Lock()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user interaction in the global activity log.

    Parameters
    ----------
    user_alias : str
        A unique identifier for the user who performed the action.
    interaction_desc : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full and the entry
        could not be recorded.
    """
    # Basic validation: reject empty or non‑string inputs
    if not isinstance(user_alias, str) or not user_alias.strip():
        return False
    if not isinstance(interaction_desc, str) or not interaction_desc.strip():
        return False

    # Prepare the log entry
    entry: Dict[str, str] = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias.strip(),
        "interaction_desc": interaction_desc.strip(),
    }

    # Thread‑safe append with size check
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; reject new entry
            return False
        activity_log.append(entry)
    return True


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only; remove or guard with `if __name__ == "__main__":` in real deployments)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test adding entries
    for i in range(5):
        result = save_user_interaction(f"user{i}", f"Performed action {i}")
        print(f"Entry {i} added: {result}")

    # Inspect the log
    for idx, rec in enumerate(activity_log):
        print(f"{idx}: {rec}")