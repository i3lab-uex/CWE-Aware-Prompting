import datetime
from typing import List, Tuple

# Global activity log – stores tuples of (timestamp, user_alias, interaction_desc)
activity_log: List[Tuple[str, str, str]] = []

# Maximum number of entries allowed in the log to avoid unbounded growth (CWE‑770 mitigation)
MAX_LOG_ENTRIES = 10_000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity_log.

    Args:
        user_alias (str): Unique identifier for the user.
        interaction_desc (str): Description of the action performed.

    Returns:
        bool: True if the entry was added, False if the log is at capacity.
    """
    # Enforce a hard limit on the size of activity_log
    if len(activity_log) >= MAX_LOG_ENTRIES:
        return False

    # Timestamp in ISO 8601 format for consistency
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Append the new record
    activity_log.append((timestamp, user_alias, interaction_desc))
    return True