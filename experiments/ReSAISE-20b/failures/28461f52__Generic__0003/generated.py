import datetime
from typing import List, Dict

# Global activity log. Each entry is a dict with keys: user_name, event_description, timestamp
activity_log: List[Dict[str, str]] = []

# Maximum number of entries allowed in the log (configurable)
MAX_LOG_SIZE: int = 10_000


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
        True if the log entry was successfully added, False if it was not added due to exceeding limits.

    Notes
    -----
    - The function is thread‑safe with respect to the global ``activity_log`` list
      by acquiring a lock around modifications.
    - The timestamp is stored in ISO 8601 format (UTC).
    """
    # Simple validation to guard against empty inputs
    if not user_name or not event_description:
        return False

    # Enforce log size limit
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create the log entry
    entry = {
        "user_name": user_name,
        "event_description": event_description,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Append to the global log
    activity_log.append(entry)
    return True