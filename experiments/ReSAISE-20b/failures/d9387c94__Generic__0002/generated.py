# activity_logger.py

from datetime import datetime
from typing import List, Tuple

# Global activity log (list of tuples: timestamp, account, operation)
activity_log: List[Tuple[str, str, str]] = []

# Maximum allowed entries in the log
MAX_LOG_SIZE: int = 1000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a new user activity record to the global activity_log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the record was successfully added, False if the log has reached its size limit.
    """
    # Enforce maximum size constraint
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a timestamp in ISO 8601 format
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Append the record as a tuple to avoid accidental mutation
    activity_log.append((timestamp, account, operation))
    return True