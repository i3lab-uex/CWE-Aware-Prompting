import datetime

# Global activity log list
activity_log = []

# Maximum number of records allowed in the log (arbitrary limit for safety)
MAX_LOG_SIZE = 10_000


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the record was successfully added; False if adding it would exceed
        MAX_LOG_SIZE.
    """
    # Enforce size limit to prevent uncontrolled growth
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Construct a record with a timestamp
    record = {
        "uid": uid,
        "event": event,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Append to the global log
    activity_log.append(record)
    return True