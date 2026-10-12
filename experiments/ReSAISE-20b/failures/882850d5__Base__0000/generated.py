import threading

# Global activity log list and its lock for thread safety
activity_log = []
_log_lock = threading.Lock()

# Maximum number of log entries allowed to mitigate CWE‑770
MAX_LOG_SIZE = 10_000

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
        True if the entry was added, False if the log size limit is reached.
    """
    # Basic validation to avoid empty entries
    if not user_alias or not interaction_desc:
        return False

    # Ensure atomic check‑and‑add operation
    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log size limit reached; refuse to add more entries
            return False

        # Append a new record as a tuple (timestamp, alias, description)
        activity_log.append((user_alias, interaction_desc))
    return True