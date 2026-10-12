import threading
from queue import Queue
from typing import Dict

# Global task queue and a lock for thread‑safety
task_queue: Queue = Queue()
_task_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        A dictionary containing all relevant details of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_details, dict):
        return False

    # Prevent accidental duplicate enqueues
    with _task_lock:
        # Check if the identifier is already in the queue (non‑blocking)
        # Since Queue doesn't support inspection, we maintain a set of identifiers
        # for quick look‑up.
        if not hasattr(task_queue, "_identifiers"):
            task_queue._identifiers = set()
        if task_identifier in task_queue._identifiers:
            return False  # Duplicate found

        try:
            # Enqueue the task
            task_queue.put_nowait((task_identifier, task_details))
            task_queue._identifiers.add(task_identifier)
        except Exception:
            return False

    return True