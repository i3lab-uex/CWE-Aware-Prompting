import threading

# Global activity log and its maximum allowed size.
activity_log = []
MAX_LOG_SIZE = 10_000

# A lock to guard concurrent modifications of the log.
_log_lock = threading.Lock()


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_alias : str
        Unique identifier of the user performing the action.
    interaction_desc : str
        Human‑readable description of the performed action.

    Returns
    -------
    bool
        True if the entry was added successfully, False if the log has reached its maximum size.
    """
    # Basic validation: ensure inputs are non-empty strings.
    if not isinstance(user_alias, str) or not user_alias.strip():
        return False
    if not isinstance(interaction_desc, str) or not interaction_desc.strip():
        return False

    # Build the log entry.
    entry = {
        "user_alias": user_alias.strip(),
        "interaction_desc": interaction_desc.strip(),
    }

    with _log_lock:
        # Enforce the maximum size limit to avoid uncontrolled resource consumption.
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        activity_log.append(entry)
    return True