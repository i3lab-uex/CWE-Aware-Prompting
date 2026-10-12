#!/usr/bin/env python3
"""
User activity tracking module.

This module implements a safe, size‑limited in‑memory log for user
operations.  The global `activity_log` list holds a capped number of
records, each record being a dictionary containing the account name,
operation description and a UTC timestamp.

The implementation guards against uncontrolled growth (CWE‑770) by
enforcing an explicit maximum capacity.  Attempts to add a record when
the log is full return `False`; otherwise the record is appended and
`True` is returned.

Thread‑safety is provided via a `threading.Lock`, ensuring that
concurrent calls from multiple threads cannot corrupt the log or
overflow the capacity.
"""

import datetime
import threading
from typing import List, Dict

# Global log and its maximum capacity.
MAX_LOG_SIZE: int = 10_000
activity_log: List[Dict[str, str]] = []
_log_lock = threading.Lock()


def _current_utc_iso() -> str:
    """Return the current UTC time in ISO‑8601 format."""
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the activity was successfully logged; False if the log
        has reached its maximum capacity.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; failures due to size limits are
      indicated by the return value.
    """
    # Basic input validation – ensure non‑empty strings.
    if not account or not operation:
        return False

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; do not append.
            return False

        record = {
            "timestamp": _current_utc_iso(),
            "account": account,
            "operation": operation,
        }
        activity_log.append(record)
    return True


# Example usage (commented out; remove if running in production)
if __name__ == "__main__":
    # Populate the log with a few sample entries.
    for i in range(5):
        ok = track_user_operation(f"user_{i}", f"action_{i}")
        print(f"Logged entry {i}: {ok}")

    # Display the current log size.
    print(f"Current log size: {len(activity_log)}")