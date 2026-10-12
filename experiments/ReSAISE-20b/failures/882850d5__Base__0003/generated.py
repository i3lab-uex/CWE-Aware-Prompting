# activity_logger.py

"""
Activity Logger Module

This module provides a simple in‑memory logging facility for user interactions.
It implements a resource limit to mitigate CWE‑770 (unbounded allocation).
"""

from typing import List, Dict
import time

# Global activity log list
activity_log: List[Dict[str, str]] = []

# Maximum number of log entries allowed. Adjust as needed.
_MAX_LOG_ENTRIES: int = 10_000


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
        True if the entry was added, False if the log is at capacity.
    """
    global activity_log

    # Enforce maximum size to prevent runaway memory usage
    if len(activity_log) >= _MAX_LOG_ENTRIES:
        return False

    # Create a log entry with a timestamp
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    activity_log.append(entry)
    return True