import datetime
import threading

# Global activity log and lock for thread‑safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of entries allowed in the log to prevent uncontrolled growth
_MAX_LOG_SIZE = 10_000


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
        True if the entry was added; False if the log has reached its limit.

    Notes
    -----
    - The function is thread‑safe.
    - Each log entry is a dictionary containing:
        * `timestamp`: ISO‑formatted UTC datetime string
        * `user_alias`
        * `interaction_desc`
    """
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "user_alias": user_alias,
        "interaction_desc": interaction_desc,
    }

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not add new entries once the limit is reached
            return False

        activity_log.append(entry)
        return True