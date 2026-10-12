import threading

# Global activity log and its maximum size
activity_log = []
MAX_LOG_SIZE = 10_000

# Thread‑safe lock for concurrent access
_log_lock = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Human‑readable text describing the action.

    Returns
    -------
    bool
        True if the event was added, False if the log is at capacity.
    """
    # Basic validation to avoid storing empty data
    if not uid or not description:
        return False

    with _log_lock:
        # Reject new events when the log has reached its maximum size
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        # Append a tuple of (uid, description); could extend with timestamp if needed
        activity_log.append((uid, description))
        return True