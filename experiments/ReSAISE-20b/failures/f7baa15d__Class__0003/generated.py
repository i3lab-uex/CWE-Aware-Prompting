import threading
from queue import Queue, Full

# Global task queue with a maximum size to avoid uncontrolled resource consumption
MAX_QUEUE_SIZE = 1000          # Adjust as appropriate for your environment
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Optional: keep track of task IDs to ensure uniqueness
_task_ids_lock = threading.Lock()
_registered_task_ids = set()

def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global queue for later processing.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic validation
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Ensure task_id uniqueness (optional but helps prevent accidental duplicates)
    with _task_ids_lock:
        if task_id in _registered_task_ids:
            return False
        _registered_task_ids.add(task_id)

    try:
        # Non-blocking put to avoid blocking the caller
        task_queue.put_nowait((task_id, task_data))
    except Full:
        # Queue is full; rollback the registration
        with _task_ids_lock:
            _registered_task_ids.discard(task_id)
        return False

    return True