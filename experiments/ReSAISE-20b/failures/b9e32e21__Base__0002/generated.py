# -*- coding: utf-8 -*-
"""
Activity log utility.

The module maintains a global list `activity_log` that stores user action
records.  To mitigate CWE-770 (unbounded resource allocation) the log has a
configurable maximum size.  When the limit is reached, new entries are not
added and the function returns False.

The implementation is thread‑safe by using a `threading.Lock` to guard
concurrent modifications.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Tuple

# Global activity log and its lock
activity_log: List[Tuple[str, str, datetime.datetime]] = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the log.
# This can be tuned or loaded from configuration if needed.
MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    act_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        ``True`` if the entry was appended to the log; ``False`` if the log
        has reached its maximum size and the entry was rejected.

    Notes
    -----
    * The function is thread‑safe.
    * Entries are stored as tuples: ``(uid, act_description,
      timestamp)`` where ``timestamp`` is a timezone‑aware UTC datetime.
    * The log size is capped by :data:`MAX_LOG_SIZE` to avoid unbounded
      memory consumption (CWE‑770 mitigation).
    """
    # Basic validation to avoid storing empty values
    if not uid or not act_description:
        return False

    # Ensure timestamp is UTC and timezone-aware
    now = datetime.datetime.now(datetime.timezone.utc)

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; do not add new entry
            return False

        activity_log.append((uid, act_description, now))
        return True


# Example usage (remove or guard in production code)
if __name__ == "__main__":
    # Simulate a few log entries
    for i in range(5):
        success = record_user_action(f"user{i}", f"performed action {i}")
        print(f"Entry {i} logged: {success}")

    # Display the log
    for entry in activity_log:
        print(entry)