import threading

# Global activity log and its maximum allowed size.
activity_log: list[dict] = []
_MAX_LOG_SIZE = 10_000

# Lock to make log updates thread‑safe.
_log_lock = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user event in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        ``True`` if the event was appended to the log,
        ``False`` if the log had reached its maximum size and
        the event was rejected.
    """
    # Basic validation to avoid injection of malicious data into logs.
    if not isinstance(uid, str) or not isinstance(description, str):
        return False

    event = {
        "uid": uid,
        "description": description,
        # Use UTC timestamp for consistency.
        "timestamp": _current_utc_timestamp(),
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entry to prevent uncontrolled resource consumption.
            return False
        activity_log.append(event)

    return True


def _current_utc_timestamp() -> str:
    """Return an ISO‑8601 formatted UTC timestamp."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()