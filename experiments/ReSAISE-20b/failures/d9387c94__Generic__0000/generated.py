#!/usr/bin/env python3
"""
User activity tracking module.

This module provides a simple in‑memory activity log with a size limit.
It is designed for lightweight monitoring and audit purposes.
"""

import datetime
from typing import List, Dict

# Global activity log (in‑memory list).  Each entry is a dict.
activity_log: List[Dict[str, str]] = []

# Maximum number of records allowed in the log.  Adjust as needed.
MAX_LOG_SIZE: int = 10_000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Record a user activity in the global activity_log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was appended successfully,
        False if the log size limit would be exceeded.
    """
    # Guard against exceeding the maximum allowed size
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Build the activity record
    record = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "account": account,
        "operation": operation,
    }

    # Append to the global log
    activity_log.append(record)
    return True