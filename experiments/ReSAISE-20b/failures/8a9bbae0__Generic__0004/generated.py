# task_queue.py

from queue import Queue, Full
import threading

# Global thread‑safe queue for tasks
task_queue: Queue = Queue()

# A set to keep track of identifiers already in the queue for quick duplicate checks
_task_ids_lock = threading.Lock()
_enqueued_task_ids: set[str] = set()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        Dictionary containing task specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    # Ensure the task identifier is unique in the queue
    with _task_ids_lock:
        if task_identifier in _enqueued_task_ids:
            # Duplicate identifier; reject the task
            return False

    try:
        # Construct a tuple or custom object representing the task
        task = (task_identifier, task_details)

        # Attempt to put the task into the queue
        task_queue.put(task, block=False)  # non‑blocking

    except Full:
        # Queue is full; cannot enqueue
        return False
    except Exception:
        # Any other exception should be swallowed to satisfy the contract
        return False

    # Register the identifier as enqueued
    with _task_ids_lock:
        _enqueued_task_ids.add(task_identifier)

    return True