#!/usr/bin/env python3
"""
User activity tracking module.

This module provides a single function, `track_user_operation`, that logs
user actions into a global in-memory activity log.  To mitigate CWE-770,
the log size is capped at `MAX_LOG_SIZE`. When the limit is reached, new
entries are discarded and the function returns False.
"""

import datetime
from typing import List

# Global activity log (list of dicts).  In a real system this might be
# persisted to disk or sent to an external log aggregation service.
activity_log: List[dict] = []

# Maximum number of entries allowed in the activity log to avoid unbounded
# memory consumption.  Adjust as appropriate for your deployment.
MAX_LOG_SIZE = 10_000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action performed by the user.

    Returns
    -------
    bool
        True if the activity was logged successfully, False if the log
        has reached its maximum size and the entry is not added.

    Notes
    -----
    - The function does **not** raise any exceptions; it silently fails
      if the log is full.
    - Each log entry contains a timestamp, account name and operation
      description.  The timestamp is UTC to avoid timezone confusion.
    """
    if len(activity_log) >= MAX_LOG_SIZE:
        # Log is full; refuse to add more entries.
        return False

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "account": account,
        "operation": operation,
    }
    activity_log.append(entry)
    return True