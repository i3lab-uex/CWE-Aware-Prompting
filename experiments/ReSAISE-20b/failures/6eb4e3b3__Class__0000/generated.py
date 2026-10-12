import threading

# Maximum number of activity records that can be stored.
MAX_LOG_SIZE = 10_000

# Global activity log and a lock for thread‑safe access.
activity_log = []
_log_lock = threading.Lock()


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action to the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    event : str
        Description of the action performed by the user.

    Returns
    -------
    bool
        True if the record was added successfully, False if adding it would exceed
        MAX_LOG_SIZE.

    Notes
    -----
    - Thread‑safe via a global lock.
    - The function never raises an exception; it simply refuses to log if the
      size limit would be breached (CWE‑400 protection).
    """
    # Basic validation: ensure inputs are strings.
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Construct the record.  We keep it simple; in a real system you might
    # include timestamps, IP addresses, etc.
    record = {"uid": uid, "event": event}

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Exceeds allowed size; do not log to avoid uncontrolled growth.
            return False
        activity_log.append(record)
    return True