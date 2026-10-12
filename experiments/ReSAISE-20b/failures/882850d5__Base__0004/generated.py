import threading
from datetime import datetime

# Global activity log list and its lock for thread‑safety
activity_log: list[dict] = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the activity log
_MAX_LOG_SIZE: int = 10_000

def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Records a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user.
    interaction_desc : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if the log has reached its limit.
    """
    # Basic validation to avoid storing empty entries
    if not user_alias or not interaction_desc:
        return False

    # Build the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log limit reached – refuse to add more entries
            return False
        activity_log.append(entry)

    return True