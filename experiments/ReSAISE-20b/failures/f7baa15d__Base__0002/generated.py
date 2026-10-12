import threading
from queue import Queue, Full

# ------------------------------------------------------------------
# Global data structures
# ------------------------------------------------------------------

# Max number of tasks that can be queued at once (prevents resource exhaustion)
_MAX_QUEUE_SIZE = 10_000

# Thread‑safe queue to hold tasks
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=_MAX_QUEUE_SIZE)

# Set to keep track of task IDs that are currently queued
# (helps avoid duplicate entries)
_task_id_set: set[str] = set()
_task_id_lock = threading.Lock()

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False if the queue is full or the task_id already exists.
    """
    # Basic validation
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Ensure uniqueness of task_id
    with _task_id_lock:
        if task_id in _task_id_set:
            return False
        # Reserve the ID before attempting to enqueue
        _task_id_set.add(task_id)

    try:
        # Try to put the task into the queue without blocking
        task_queue.put_nowait((task_id, task_data))
    except Full:
        # Queue is full – release the reserved ID and signal failure
        with _task_id_lock:
            _task_id_set.discard(task_id)
        return False

    # Task successfully queued
    return True