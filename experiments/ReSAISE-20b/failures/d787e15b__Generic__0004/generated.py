import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=1000)

# Lock to guard against duplicate task references if needed
_task_lock = threading.Lock()
_registered_tasks = set()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Dictionary of task parameters.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Avoid duplicate entries in a concurrent environment
    with _task_lock:
        if task_reference in _registered_tasks:
            return False
        _registered_tasks.add(task_reference)

    try:
        # Queue may block if full; we use a short timeout to avoid deadlocks
        task_queue.put((task_reference, parameters), timeout=0.1)
    except Full:
        # Queue is full; remove the reference from the set to allow retry later
        with _task_lock:
            _registered_tasks.discard(task_reference)
        return False

    return True