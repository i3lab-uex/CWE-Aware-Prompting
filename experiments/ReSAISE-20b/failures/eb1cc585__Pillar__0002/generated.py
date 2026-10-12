import threading
from datetime import datetime

# Global activity log and configuration
MAX_LOG_SIZE = 10_000          # Maximum number of entries allowed in the log
activity_log: list[dict] = []  # Central repository for user activity records
log_lock = threading.Lock()    # Protects concurrent access to the log


def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Records a user action in the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action performed.

    Returns
    -------
    bool
        True if the action was logged successfully, False if the log is at capacity.
    """
    # Basic type validation to avoid malformed entries
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "event": event,
    }

    with log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log capacity reached – reject the entry
            return False

        activity_log.append(entry)
        return True