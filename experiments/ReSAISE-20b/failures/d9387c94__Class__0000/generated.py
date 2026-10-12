import time

# Global activity log with a hard limit to prevent uncontrolled resource consumption.
MAX_LOG_SIZE = 10_000
activity_log: list[dict] = []


def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action performed by the user.

    Returns
    -------
    bool
        True if the record was added successfully, False if adding would exceed MAX_LOG_SIZE.
    """
    # Guard against excessive growth
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a lightweight record with minimal data
    record = {
        "timestamp": int(time.time()),  # Unix epoch seconds
        "account": account,
        "operation": operation,
    }

    activity_log.append(record)
    return True