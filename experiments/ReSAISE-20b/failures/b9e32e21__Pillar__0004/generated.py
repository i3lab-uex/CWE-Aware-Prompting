import threading
from typing import List

# Global activity log list and a lock for thread‑safety.
activity_log: List[dict] = []
_activity_lock = threading.Lock()

# Maximum number of records that the log can hold.
_MAX_LOG_SIZE: int = 10_000


def _sanitize(text: str) -> str:
    """
    Basic sanitisation to prevent injection attacks when the log is later displayed
    or processed. This function escapes newlines and control characters.
    """
    if not isinstance(text, str):
        return ""
    # Replace non‑printable characters with their Unicode name.
    sanitized = "".join(
        c if 32 <= ord(c) < 127 else f"\\u{ord(c):04x}" for c in text
    )
    return sanitized


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user who performed the action.
    act_description : str
        Textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added, False if it was not added due to
        exceeding the maximum allowed size.

    Notes
    -----
    - The function is thread‑safe.
    - A simple size limit prevents uncontrolled growth of the log (CWE‑664).
    """
    # Validate input types.
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Sanitize inputs to avoid storing problematic characters.
    uid_sanitized = _sanitize(uid)
    act_sanitized = _sanitize(act_description)

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log is full; refuse to add more entries.
            return False
        activity_log.append(
            {
                "uid": uid_sanitized,
                "action": act_sanitized,
                # Optionally include a timestamp for audit purposes.
                "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            }
        )
    return True