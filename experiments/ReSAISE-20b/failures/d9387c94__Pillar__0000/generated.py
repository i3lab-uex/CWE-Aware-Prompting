#!/usr/bin/env python3
"""
Activity tracking module.

This module provides a thread‑safe function `track_user_operation` that records
user actions in a global activity log.  The log is bounded by a maximum size;
attempts to exceed this limit are rejected and the function returns `False`.

The implementation follows best practices for resource control (CWE‑664) by
ensuring that the log is never over‑allocated, and by guarding all mutations
with a lock to prevent race conditions in concurrent environments.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict

# Global activity log and its configuration.
MAX_LOG_SIZE: int = 10_000          # maximum number of entries allowed
activity_log: List[Dict[str, str]] = []  # list of activity records

# Lock to guard concurrent access to the global log.
_log_lock = threading.Lock()


def track_user_operation(account: str, operation: str) -> bool:
    """
    Record a user operation in the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action performed.

    Returns
    -------
    bool
        ``True`` if the activity was appended successfully, ``False`` if the log
        has reached its maximum size and the operation could not be recorded.

    Notes
    -----
    * The function is thread‑safe: a global lock protects the log from concurrent
      modifications.
    * The function does **not** raise exceptions.  If the log is full, it simply
      returns ``False``.
    * The timestamp is captured in ISO 8601 format with UTC timezone.

    Example
    -------
    >>> track_user_operation('alice', 'login')
    True
    """
    # Validate inputs quickly (optional but helps catch obvious misuse)
    if not isinstance(account, str) or not isinstance(operation, str):
        return False

    # Prepare the record
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    record: Dict[str, str] = {
        "account": account,
        "operation": operation,
        "timestamp": timestamp,
    }

    # Safely append to the log
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full – reject the new entry
            return False

        activity_log.append(record)
        return True


# The following test harness is only executed when the module is run directly.
if __name__ == "__main__":
    # Simple demonstration and sanity check
    assert track_user_operation("user1", "created_account") is True
    assert len(activity_log) == 1

    # Fill the log to its limit and confirm rejection
    MAX_LOG_SIZE = 2  # shrink for quick test
    activity_log.clear()
    assert track_user_operation("u1", "op1") is True
    assert track_user_operation("u2", "op2") is True
    # Next operation should fail due to size limit
    assert track_user_operation("u3", "op3") is False

    print("All tests passed.")