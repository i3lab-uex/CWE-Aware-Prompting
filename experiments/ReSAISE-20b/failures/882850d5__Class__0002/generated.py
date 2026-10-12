import threading

# Global activity log and configuration
activity_log: list[tuple[str, str]] = []
_MAX_LOG_SIZE = 1000           # Maximum number of log entries allowed
_log_lock = threading.Lock()   # Ensure thread‑safe access to the log


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_alias : str
        A unique identifier for the user who performed the action.
    interaction_desc : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added, False if adding it would exceed
        the maximum allowed size of the activity_log.
    """
    # Basic validation to avoid storing malformed data
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        return False

    # Enforce log size limit to prevent uncontrolled resource consumption (CWE‑400)
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append((user_alias, interaction_desc))
    return True