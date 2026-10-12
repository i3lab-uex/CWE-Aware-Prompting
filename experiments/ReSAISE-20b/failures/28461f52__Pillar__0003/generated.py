import threading
from collections import deque

# Global activity log – stores tuples of (user_name, event_description)
# Using a deque with a maximum length ensures old entries are automatically discarded,
# preventing unbounded growth and potential resource exhaustion.
MAX_LOG_SIZE = 10_000
activity_log: deque[tuple[str, str]] = deque(maxlen=MAX_LOG_SIZE)

# A lock to guard concurrent access to the activity log (CWE‑664 mitigation).
_log_lock = threading.Lock()


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user performing the action.
    event_description : str
        Textual description of the action.

    Returns
    -------
    bool
        True if the entry was added; False if the log is at its maximum capacity.
    """
    # Validate inputs – guard against malicious data (e.g., overly long strings).
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False

    # Truncate strings to reasonable lengths to avoid runaway memory usage.
    user_name = user_name[:256]
    event_description = event_description[:2048]

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # Log is full; do not add new entry.
            return False
        activity_log.append((user_name, event_description))
    return True