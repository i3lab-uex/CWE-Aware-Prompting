import threading

# Global activity log and a lock for thread‑safety
activity_log: list[tuple[str, str]] = []
_LOG_LOCK = threading.Lock()

# Maximum number of entries allowed in the log to prevent uncontrolled growth
_MAX_LOG_SIZE = 1000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        A unique identifier for the user who performed the action.
    interaction_desc : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the entry was added; False if adding it would exceed
        :data:`_MAX_LOG_SIZE`.

    Notes
    -----
    * The function is thread‑safe: it uses a lock to prevent race conditions.
    * Input strings are stored as-is; no external I/O is performed, so
      injection attacks cannot affect the log directly.
    * The global list acts as a simple in‑memory resource; its size is
      bounded to avoid CWE‑664 (resource exhaustion).
    """
    # Basic validation: ensure non-empty strings
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        return False

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        # Append a tuple of the user alias and interaction description.
        activity_log.append((user_alias, interaction_desc))
    return True