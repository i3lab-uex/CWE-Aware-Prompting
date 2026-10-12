import threading
from queue import Queue
from typing import Dict, Any

# Global task queue and a set to keep track of enqueued identifiers
task_queue: Queue = Queue()
_enqueued_ids_lock = threading.Lock()
_enqueued_ids = set()

def enqueue_task(task_identifier: str, task_details: Dict[str, Any]) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_details : dict
        A dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_details, dict):
        return False

    # Prevent duplicate identifiers and guard against race conditions
    with _enqueued_ids_lock:
        if task_identifier in _enqueued_ids:
            # Duplicate found – do not enqueue
            return False
        # Mark identifier as reserved
        _enqueued_ids.add(task_identifier)

    try:
        # Enqueue the task as a tuple (id, details)
        task_queue.put((task_identifier, task_details))
    except Exception:
        # If enqueue fails for any reason, clean up the reserved id
        with _enqueued_ids_lock:
            _enqueued_ids.discard(task_identifier)
        return False

    # Successful enqueue
    return True