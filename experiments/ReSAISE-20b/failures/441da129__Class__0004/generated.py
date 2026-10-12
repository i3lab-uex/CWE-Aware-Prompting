# log_user_event.py

"""
A lightweight activity logging utility.

This module defines a single function `log_user_event` that appends user actions
to a global list named `activity_log`. The function enforces a configurable size
limit to mitigate CWE-400 (Uncontrolled Resource Consumption).  The log is kept
in memory; for production use, a more robust persistence layer (e.g. database,
file rotation, or external logging service) should be employed.

Author: OpenAI ChatGPT
"""

# --------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------- #

from datetime import datetime
from typing import List, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Maximum number of log entries to keep in memory.
MAX_LOG_SIZE: int = 10_000

# --------------------------------------------------------------------------- #
# Global activity log
# --------------------------------------------------------------------------- #

# Each entry is a tuple: (timestamp, user_key, action_details)
activity_log: List[Tuple[datetime, str, str]] = []

# --------------------------------------------------------------------------- #
# Logging function
# --------------------------------------------------------------------------- #

def log_user_event(user_key: str, action_details: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_key : str
        Unique identifier for the user performing the action.
    action_details : str
        Textual description of the action undertaken.

    Returns
    -------
    bool
        True if the event was added to `activity_log`; False if the log has reached
        its configured maximum size and the event was rejected.

    Notes
    -----
    - The function is thread‑unsafe; if concurrent access is required, callers
      should provide appropriate synchronization (e.g., a threading.Lock).
    - No exceptions are raised; the function simply returns False when the
      size limit is exceeded.
    """
    # Basic validation: ensure inputs are strings
    if not isinstance(user_key, str) or not isinstance(action_details, str):
        # Reject invalid input silently; return False
        return False

    # Enforce log size limit to prevent uncontrolled memory growth.
    if len(activity_log) >= MAX_LOG_SIZE:
        # Log is full; reject new entry.
        return False

    # Append the event with a timestamp
    activity_log.append((datetime.utcnow(), user_key, action_details))
    return True

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     for i in range(12_000):
#         success = log_user_event(f"user{i}", f"action {i}")
#         if not success:
#             print(f"Log full at iteration {i}")
#             break