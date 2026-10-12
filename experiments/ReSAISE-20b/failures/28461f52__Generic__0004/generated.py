import time
from typing import List, Dict, Any
from threading import Lock

# Global activity log and associated lock for thread‑safety.
activity_log: List[Dict[str, Any]] = []
_LOG_LOCK = Lock()

# Optional configuration constants.
_MAX_LOG_SIZE: int = 10_000          # Maximum number of entries to keep
_MAX_EVENT_LENGTH: int = 512         # Maximum allowed length for event_description


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        A unique identifier for the user who performed the action.
    event_description : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added, False if it could not be added
        because the log exceeded its configured size limit.

    Notes
    -----
    - The function performs minimal validation on the inputs to avoid obvious
      security issues such as overly long strings or incorrect types.
    - The global log is protected by a lock to make it safe for concurrent use
      in multi‑threaded environments.
    - The function does not raise any exceptions; it simply returns False if the
      entry cannot be added.
    """
    # Basic type checks to guard against misuse; silently ignore invalid input.
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Truncate excessively long event descriptions to avoid runaway memory usage.
    if len(event_description) > _MAX_EVENT_LENGTH:
        event_description = event_description[:_MAX_EVENT_LENGTH]

    entry = {
        "timestamp": time.time(),          # Unix epoch timestamp
        "user_name": user_name,
        "event_description": event_description,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Optionally, could discard oldest entries here; for now we refuse to add.
            return False
        activity_log.append(entry)

    return True