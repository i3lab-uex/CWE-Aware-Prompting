import datetime

# Global activity log (list of dicts)
activity_log = []

# Maximum allowed entries in the log
MAX_LOG_SIZE = 10_000


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    task : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was successfully logged.
        False if the log has reached MAX_LOG_SIZE and the record is not added.
    """
    # Guard against exceeding maximum log size
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a record with a timestamp (ISO 8601 format)
    record = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_identifier": user_identifier,
        "task": task,
    }

    # Append to the global log
    activity_log.append(record)

    return True