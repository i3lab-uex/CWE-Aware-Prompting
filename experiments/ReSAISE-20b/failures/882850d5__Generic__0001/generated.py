import threading
from datetime import datetime

# Global activity log and its configuration
activity_log: list[dict] = []
_MAX_LOG_SIZE: int = 10_000          # Maximum number of entries allowed
_log_lock = threading.Lock()        # Ensure thread‑safe modifications

def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user.
    interaction_desc : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log has reached its maximum size.
    """
    # Basic validation of inputs
    if not isinstance(user_alias, str) or not user_alias:
        raise ValueError("user_alias must be a non‑empty string")
    if not isinstance(interaction_desc, str) or not interaction_desc:
        raise ValueError("interaction_desc must be a non‑empty string")

    # Construct the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    # Thread‑safe addition with size check
    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            return False
        activity_log.append(entry)
    return True