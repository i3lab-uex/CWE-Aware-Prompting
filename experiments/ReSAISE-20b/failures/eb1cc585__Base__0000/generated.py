import threading
from datetime import datetime

# Global activity log and its configuration
activity_log = []
MAX_LOG_ENTRIES = 10_000          # Limit to prevent uncontrolled growth
LOG_LOCK = threading.Lock()       # Ensure thread‑safe access

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the record was added, False if the log has reached its maximum size.
    """
    # Validate input types
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        return False

    # Construct the log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_identifier,
        "event": event
    }

    with LOG_LOCK:
        if len(activity_log) >= MAX_LOG_ENTRIES:
            # Log is full; reject the new entry
            return False

        activity_log.append(entry)
        return True