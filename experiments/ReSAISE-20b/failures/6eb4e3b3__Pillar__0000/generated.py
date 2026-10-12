import datetime
import threading

# Global activity log (list of dicts)
activity_log = []
# Maximum number of records allowed in the log
MAX_LOG_SIZE = 10_000

# Lock to guard concurrent access to activity_log
_log_lock = threading.Lock()


def record_user_action(uid: str, event: str) -> bool:
    """
    Append a user action record to the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    event : str
        Description of the specific action taken by the user.

    Returns
    -------
    bool
        True if the record was successfully logged, False if the log is full.
    """
    # Ensure inputs are strings (defensive programming)
    uid = str(uid) if uid is not None else ""
    event = str(event) if event is not None else ""

    with _log_lock:
        # Check size limit before appending
        if len(activity_log) >= MAX_LOG_SIZE:
            return False

        # Record structure: timestamp, uid, event
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "uid": uid,
            "event": event,
        }
        activity_log.append(record)
    return True