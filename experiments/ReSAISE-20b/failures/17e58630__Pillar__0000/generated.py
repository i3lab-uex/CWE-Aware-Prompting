import threading
from collections import deque
from typing import Dict, Tuple

# Global task queue and its lock for thread‑safe access
_task_queue: deque[Tuple[str, Dict]] = deque()
_task_lock = threading.RLock()

def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Task parameters and other relevant information.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.

    Notes
    -----
    The function is thread‑safe. It never raises an exception; any unexpected
    error results in a graceful False return.
    """
    try:
        # Basic validation to avoid inserting malformed entries
        if not isinstance(identifier, str) or not identifier:
            return False
        if not isinstance(details, dict):
            return False

        with _task_lock:
            # Append the task as a tuple to preserve order
            _task_queue.append((identifier, details))

        return True

    except Exception:
        # Log the exception if a logging system is available
        # For this example we silently return False
        return False

# Expose the queue for external consumers (read‑only view)
def get_task_queue_snapshot() -> Tuple[Tuple[str, Dict], ...]:
    """
    Return a snapshot of the current queue state.
    This function is read‑only and thread‑safe.
    """
    with _task_lock:
        return tuple(_task_queue)