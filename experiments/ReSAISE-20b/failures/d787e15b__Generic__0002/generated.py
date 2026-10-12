import threading
from queue import Queue, Full

# Global task storage structures
task_queue: Queue = Queue()
_registered_tasks: set[str] = set()
_lock = threading.RLock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task for future execution.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    with _lock:
        # Ensure uniqueness of task_reference
        if task_reference in _registered_tasks:
            return False

        # Attempt to enqueue the task
        try:
            task_queue.put_nowait((task_reference, parameters))
        except Full:
            # Queue is full; cannot add new task
            return False

        # Mark as registered
        _registered_tasks.add(task_reference)
        return True