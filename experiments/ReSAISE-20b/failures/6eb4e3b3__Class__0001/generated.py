import datetime
import threading

# Global activity log and configuration
activity_log: list[dict] = []
LOG_MAX_ENTRIES = 10_000          # maximum number of entries allowed
_log_lock = threading.Lock()      # protects concurrent access

def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the action taken.

    Returns
    -------
    bool
        True if the record was appended successfully, False otherwise
        (e.g., when the log has reached its maximum size).

    Notes
    -----
    - The function is thread‑safe via a lock.
    - It enforces a hard cap on the number of stored records to
      mitigate CWE‑400 (Uncontrolled Resource Consumption).
    - The timestamp is recorded in UTC to avoid time‑zone issues.
    """
    # Basic validation of inputs
    if not isinstance(uid, str) or not isinstance(event, str):
        return False

    # Prepare the record
    record = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "uid": uid,
        "event": event
    }

    with _log_lock:
        if len(activity_log) >= LOG_MAX_ENTRIES:
            # Log is full; reject new entry
            return False

        activity_log.append(record)
        return True