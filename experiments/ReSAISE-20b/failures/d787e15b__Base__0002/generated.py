import threading
from queue import Queue, Full

# Global task queue with a sane maximum size to mitigate CWE‑770
MAX_QUEUE_SIZE = 10_000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Global set to track registered task references and avoid duplicates
_registered_task_refs = set()
_ref_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task for later execution.

    Args:
        task_reference (str): Unique identifier of the task.
        parameters (dict): Parameters describing the task.

    Returns:
        bool: True if the task was successfully queued, False otherwise.
    """
    # Validate input types
    if not isinstance(task_reference, str) or not isinstance(parameters, dict):
        return False

    # Ensure uniqueness and thread safety
    with _ref_lock:
        if task_reference in _registered_task_refs:
            # Duplicate reference; do not enqueue again
            return False
        # Reserve the reference before attempting to enqueue
        _registered_task_refs.add(task_reference)

    try:
        # Attempt to put the task into the queue without blocking
        task_queue.put_nowait((task_reference, parameters))
    except Full:
        # Queue is full; release the reserved reference
        with _ref_lock:
            _registered_task_refs.remove(task_reference)
        return False

    # Task successfully queued
    return True