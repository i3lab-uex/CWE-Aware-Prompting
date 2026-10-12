import threading

# Global activity log with a maximum capacity to prevent uncontrolled growth.
MAX_LOG_SIZE = 10_000
activity_log: list[tuple[str, str]] = []
log_lock = threading.Lock()


def save_user_event(user_identifier: str, task: str) -> bool:
    """
    Append a user activity record to the global `activity_log`.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user performing the action.
    task : str
        A description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was added; False if adding would exceed MAX_LOG_SIZE.
    """
    # Normalise inputs to avoid accidental injection or malformed entries
    uid = str(user_identifier).strip()
    act = str(task).strip()

    if not uid or not act:
        # Reject empty values to keep the log clean
        return False

    with log_lock:  # Ensure atomicity in a multi‑threaded environment
        if len(activity_log) >= MAX_LOG_SIZE:
            return False  # Do not exceed the pre‑defined limit

        activity_log.append((uid, act))
    return True