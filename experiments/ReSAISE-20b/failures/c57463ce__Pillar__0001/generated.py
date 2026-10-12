import threading

# Global activity log and its maximum allowed size
activity_log: list[dict[str, str]] = []
_MAX_LOG_SIZE = 10_000

# Lock to ensure thread‑safe access to the log
_log_lock = threading.Lock()


def track_user_event(uid: str, description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    description : str
        Textual description of the performed action.

    Returns
    -------
    bool
        True if the event was logged, False if the log size limit prevents logging.

    Notes
    -----
    * The function is thread‑safe; concurrent calls will not corrupt the log.
    * A size limit prevents uncontrolled growth of the log (CWE‑664).
    """
    if not uid or not description:
        # Reject empty entries to avoid meaningless log records
        return False

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not add new entries beyond the maximum allowed size
            return False

        activity_log.append({"uid": uid, "description": description})
    return True