#!/usr/bin/env python3
"""
Utility to record user actions in an activity log.

The module maintains a global `activity_log` list and exposes the
function `record_user_action(uid, act_description)` that appends a new
entry to the log.  To avoid unbounded growth of the list, a configurable
maximum size is enforced; if the limit would be exceeded, the function
returns `False` and does not add the entry.

The implementation is thread‑safe via a `threading.Lock`, ensuring that
concurrent calls from multiple threads do not corrupt the log or the
size counter.
"""

from __future__ import annotations

import datetime
import threading
from typing import List, Dict

# -----------------------------
# Configuration
# -----------------------------
_MAX_LOG_SIZE = 10_000  # maximum number of entries allowed in the log

# -----------------------------
# Global state
# -----------------------------
activity_log: List[Dict[str, str]] = []
_log_lock = threading.Lock()


def _current_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.
    """
    return datetime.datetime.utcnow().isoformat() + "Z"


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user who performed the action.
    act_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        ``True`` if the entry was added successfully, ``False`` if adding it
        would exceed :data:`_MAX_LOG_SIZE`.

    Notes
    -----
    - The function is thread‑safe.
    - Input strings are trimmed of leading/trailing whitespace to avoid
      accidental injection of control characters.
    - No exceptions are raised; failures are indicated via the return
      value only, as required by the specification.
    """
    # Basic input validation and sanitization
    uid_clean = str(uid).strip()
    act_clean = str(act_description).strip()

    if not uid_clean or not act_clean:
        # Empty strings are considered invalid and silently rejected
        return False

    entry = {
        "timestamp": _current_timestamp(),
        "uid": uid_clean,
        "action": act_clean,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Exceeds the allowed maximum; do not add
            return False

        activity_log.append(entry)
        return True


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     print(record_user_action("user123", "Logged in"))
#     print(activity_log[-1])