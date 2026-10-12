import datetime

# Global activity log repository.
activity_log = []

# Maximum number of entries allowed in the log to avoid uncontrolled growth
MAX_LOG_SIZE = 10_000


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity_log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the operation.
    operation : str
        Description of the action performed by the user.

    Returns
    -------
    bool
        True if the activity was logged successfully.
        False if logging failed because the log has reached its maximum size.
    """
    # Enforce a limit on the number of stored records to mitigate CWE-770
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Construct a log entry with a timestamp
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "account": account,
        "operation": operation,
    }

    # Append the entry to the global log
    activity_log.append(entry)
    return True