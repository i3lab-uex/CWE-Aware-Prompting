import threading
from datetime import datetime

# Global activity log and a lock for thread‑safe access
activity_log: list[dict] = []
_LOG_LOCK = threading.Lock()

# Maximum number of log entries allowed to mitigate CWE‑770
_MAX_LOG_SIZE = 100_000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user.
    interaction_desc : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if adding would exceed _MAX_LOG_SIZE.
    """
    # Basic validation to avoid storing empty data
    if not user_alias or not interaction_desc:
        return False

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    with _LOG_LOCK:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Optionally, could implement a rolling log or discard oldest entries.
            return False
        activity_log.append(log_entry)

    return True