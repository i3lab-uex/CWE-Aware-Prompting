# log_user_activity.py

"""
A simple user activity logger that appends entries to a global list.
To mitigate CWE-770 (uncontrolled resource allocation), the logger enforces
a maximum number of stored log entries. Once the limit is reached, new logs
are rejected until older entries are removed manually.
"""

from datetime import datetime
from typing import List, Tuple

# Global log store (in-memory). In production this could be replaced by a
# database or persistent storage.
activity_log: List[Tuple[str, str, datetime]] = []

# Maximum number of log entries allowed. Adjust as needed for your system.
MAX_LOG_ENTRIES = 10_000


def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the action performed.

    Returns
    -------
    bool
        True if logging succeeded, False if the log size limit was reached.
    """
    # Basic validation: ensure inputs are non-empty strings
    if not isinstance(user_id, str) or not user_id.strip():
        return False
    if not isinstance(action, str) or not action.strip():
        return False

    # Enforce the maximum log size
    if len(activity_log) >= MAX_LOG_ENTRIES:
        # Reject new entries to prevent unbounded memory growth
        return False

    try:
        entry = (user_id.strip(), action.strip(), datetime.utcnow())
        activity_log.append(entry)
        return True
    except Exception:
        # In a real system, log the exception to an error monitoring service.
        return False