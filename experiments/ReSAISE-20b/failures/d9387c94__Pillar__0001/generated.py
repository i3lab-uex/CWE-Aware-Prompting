import threading
from typing import List, Tuple

# Global activity log and configuration ---------------------------------------------------------

# Maximum number of records the log may hold.  Exceeding this limit will cause new entries to be
# rejected to prevent uncontrolled memory growth.
MAX_LOG_SIZE: int = 10_000

# The activity log itself. Each entry is a tuple (account, operation).
activity_log: List[Tuple[str, str]] = []

# A lock to guard concurrent access to the log.  This protects against race conditions
# and ensures that the size check and append happen atomically.
_log_lock = threading.Lock()


def track_user_operation(account: str, operation: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    account : str
        Unique identifier for the user performing the action.
    operation : str
        Description of the action taken.

    Returns
    -------
    bool
        ``True`` if the record was added successfully, ``False`` if the log is full and
        the operation could not be recorded.

    Notes
    -----
    - The function is thread‑safe; concurrent calls from multiple threads are serialized.
    - To avoid uncontrolled memory usage, the log is capped at ``MAX_LOG_SIZE`` entries.
      When this limit is reached new records are rejected rather than appending indefinitely.
    - ``account`` and ``operation`` are converted to strings to guard against accidental
      non‑string input.  Leading/trailing whitespace is stripped for consistency.
    """
    # Normalise inputs
    account_str = str(account).strip()
    operation_str = str(operation).strip()

    with _log_lock:
        if len(activity_log) >= MAX_LOG_SIZE:
            # The log is full; reject the new entry.
            return False

        # Append the new record.  Using a tuple ensures immutability of individual entries.
        activity_log.append((account_str, operation_str))
        return True