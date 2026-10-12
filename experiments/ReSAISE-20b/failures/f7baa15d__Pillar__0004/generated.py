import threading
from queue import Queue, Full

# Global task queue (thread‑safe) and a set to track existing task IDs
task_queue: Queue = Queue(maxsize=1000)          # adjust size as needed
_task_ids_lock = threading.Lock()
_existing_task_ids: set[str] = set()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global queue.

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
    # Validate inputs
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Ensure the task ID is unique within the queue
    with _task_ids_lock:
        if task_id in _existing_task_ids:
            return False
        # Reserve the ID before putting into queue to avoid race conditions
        _existing_task_ids.add(task_id)

    try:
        # Try to enqueue the task; use a timeout to avoid blocking indefinitely
        task_queue.put((task_id, task_data), block=False)
    except Full:
        # Queue is full; release the reserved ID
        with _task_ids_lock:
            _existing_task_ids.discard(task_id)
        return False

    # Successful enqueue
    return True


# Optional: function to remove a task ID after processing (to prevent memory leak)
def _release_task_id(task_id: str) -> None:
    with _task_ids_lock:
        _existing_task_ids.discard(task_id)