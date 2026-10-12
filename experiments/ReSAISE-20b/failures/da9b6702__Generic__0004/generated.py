import datetime

# Global activity log (list of records)
activity_log = []

# Maximum number of entries allowed in the log
MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a new user event record to the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    task : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log has reached its size limit.
    """
    # Reject logging when the log is already at maximum capacity
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a record with a UTC timestamp
    record = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_identifier": user_identifier,
        "task": task,
    }

    activity_log.append(record)
    return True