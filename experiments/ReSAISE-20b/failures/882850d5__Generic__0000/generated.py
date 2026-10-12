import datetime
import threading

# Global activity log and lock for thread‑safety
activity_log: list[dict] = []
_activity_lock = threading.Lock()

# Optional limit for the number of log entries
_MAX_LOG_SIZE: int | None = 10_000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user who performed the action.
    interaction_desc : str
        Human‑readable description of the user's action.

    Returns
    -------
    bool
        ``True`` if the entry was appended to the log,
        ``False`` if the log has reached its configured maximum size.
    """
    # Basic validation
    if not isinstance(user_alias, str) or not user_alias.strip():
        raise ValueError("user_alias must be a non‑empty string")
    if not isinstance(interaction_desc, str) or not interaction_desc.strip():
        raise ValueError("interaction_desc must be a non‑empty string")

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    with _activity_lock:
        if _MAX_LOG_SIZE is not None and len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; do not add new entry
            return False

        activity_log.append(entry)
    return True