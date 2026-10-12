import threading
from typing import List

# Global activity log and its configuration
activity_log: List[dict] = []
_MAX_LOG_SIZE: int = 10_000   # maximum number of entries allowed
_log_lock = threading.Lock()  # protects concurrent access

def record_user_action(user_identifier: str, event: str) -> bool:
    """
    Record a user action into the global activity log.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user performing the action.
    event : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added; False if the log is at capacity.
    """
    # Basic validation to avoid obvious injection attacks
    if not isinstance(user_identifier, str) or not isinstance(event, str):
        raise TypeError("Both user_identifier and event must be strings")

    # Trim whitespace to keep entries tidy
    uid = user_identifier.strip()
    evt = event.strip()

    # Reject empty identifiers or events
    if not uid or not evt:
        return False

    entry = {"user": uid, "event": evt}

    with _log_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; reject new entry
            return False
        activity_log.append(entry)

    return True