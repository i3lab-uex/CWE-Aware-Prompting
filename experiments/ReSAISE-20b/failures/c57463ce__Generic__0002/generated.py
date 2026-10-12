import datetime

# Global activity log repository
activity_log = []

# Maximum allowed entries in the activity log
MAX_LOG_SIZE = 100_000


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user event in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the event was logged successfully, False if the log has reached
        its maximum allowed size.
    """
    # Enforce size limitation before attempting to log
    if len(activity_log) >= MAX_LOG_SIZE:
        return False

    # Create a safe log entry
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        # Use a trimmed description to avoid excessive memory usage
        "description": description[:1024] if len(description) > 1024 else description,
    }

    activity_log.append(event)
    return True