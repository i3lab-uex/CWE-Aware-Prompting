import datetime
from typing import List, Dict

# Global activity log list. Each entry is a dict with uid, description, and timestamp.
activity_log: List[Dict[str, str]] = []

# Optional limit for the number of stored log entries.
MAX_LOG_SIZE: int = 10_000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user who performed the action.
    act_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        True if the entry was added, False if the log is full.
    """
    # Basic input validation to avoid storing empty or malformed data
    if not uid or not act_description:
        return False

    # Enforce a maximum size to prevent uncontrolled memory growth
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a new log entry
    entry = {
        "uid": uid,
        "description": act_description,
        # Store timestamps in ISO 8601 format for consistency
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    activity_log.append(entry)
    return True