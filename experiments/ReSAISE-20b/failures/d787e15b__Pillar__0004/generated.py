import threading
from queue import Queue, Full

# Global task queue and helper structures
_task_queue: Queue = Queue(maxsize=0)  # unbounded queue for task objects
_registered_tasks: set[str] = set()    # keeps track of unique task references
_lock = threading.Lock()              # protects access to _registered_tasks

def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        Parameters associated with the task.

    Returns
    -------
    bool
        True if the task was added to the queue, False otherwise.
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    with _lock:
        # Ensure uniqueness of the task reference
        if task_reference in _registered_tasks:
            return False
        # Mark as registered before enqueuing to avoid race conditions
        _registered_tasks.add(task_reference)

    # Attempt to enqueue the task; non‑blocking to avoid deadlocks
    try:
        _task_queue.put_nowait((task_reference, parameters))
    except Full:
        # Queue is full (unlikely with maxsize=0), revert registration
        with _lock:
            _registered_tasks.discard(task_reference)
        return False

    return True