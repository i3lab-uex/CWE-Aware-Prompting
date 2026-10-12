import threading
from typing import List, Tuple

# Global activity log and its lock for thread safety
activity_log: List[Tuple[str, str]] = []
_activity_lock = threading.Lock()

# Maximum allowed entries in the activity log (CWE‑770 mitigation)
_MAX_LOG_SIZE = 10_000

def track_user_operation(account: str, operation: str) -> bool:
    """
    Append a user activity record to the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier of the user performing the action.
    operation : str
        Description of the action taken by the user.

    Returns
    -------
    bool
        True if the record was successfully added; False if adding would exceed
        the configured maximum log size.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; failures are indicated via the return value.
    """
    # Basic sanitisation: strip leading/trailing whitespace
    account_clean = str(account).strip()
    operation_clean = str(operation).strip()

    # Avoid adding empty records
    if not account_clean or not operation_clean:
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Log size limit reached; reject new entry
            return False

        activity_log.append((account_clean, operation_clean))
    return True