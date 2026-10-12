import threading

# Global activity log and a lock for thread‑safety
activity_log = []
_log_lock = threading.Lock()

# Optional limit to prevent uncontrolled growth (CWE‑400 mitigation)
_MAX_LOG_SIZE = 10_000

def log_user_activity(user_id: str, action: str) -> bool:
    """
    Append a user activity entry to the global log.

    Parameters
    ----------
    user_id : str
        Identifier of the user performing the action.
    action : str
        Description of the performed action.

    Returns
    -------
    bool
        True if the entry was added successfully, False otherwise.
    """
    # Basic input validation to avoid malformed entries
    if not isinstance(user_id, str) or not isinstance(action, str):
        return False

    entry = {"user_id": user_id, "action": action}

    try:
        with _log_lock:
            # Enforce maximum size to mitigate uncontrolled resource consumption
            if len(activity_log) >= _MAX_LOG_SIZE:
                # Remove the oldest entry (FIFO)
                activity_log.pop(0)

            activity_log.append(entry)
        return True
    except Exception:
        # Log the exception internally if needed; for now just swallow it
        return False