# activity_logger.py

import threading

# Global list to store activity logs
activity_log = []

# Maximum number of entries allowed in the log (to avoid uncontrolled resource consumption)
MAX_LOG_SIZE = 10_000

# Thread‑safety lock for concurrent access
_log_lock = threading.Lock()


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        Unique identifier for the user performing the action.
    interaction_desc : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was added; False if the log has reached its maximum size.
    """
    # Validate inputs (basic sanity check)
    if not isinstance(user_alias, str) or not isinstance(interaction_desc, str):
        return False

    with _log_lock:
        # Prevent uncontrolled growth of the log
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        # Append a timestamped entry
        activity_log.append(
            {
                "user_alias": user_alias,
                "interaction_desc": interaction_desc,
                "timestamp": _current_timestamp(),
            }
        )
    return True


def _current_timestamp() -> str:
    """Return an ISO‑8601 formatted UTC timestamp."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()