import threading

# Global activity log and its maximum allowed size.
activity_log = []
_MAX_LOG_SIZE = 1000

# Thread‑safety lock for concurrent access to the log.
_log_lock = threading.Lock()


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user who performed the action.
    interaction_desc : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was added, False if the maximum size limit
        prevented adding it.

    Notes
    -----
    - The function is thread‑safe; concurrent calls are serialized using a lock.
    - No exceptions are raised; if the log is full, the function simply returns False.
    """
    # Basic input validation – ensure we are dealing with strings.
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        # Invalid input: silently ignore and return False.
        return False

    entry = {
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log has reached its capacity; do not add the entry.
            return False
        activity_log.append(entry)
    return True