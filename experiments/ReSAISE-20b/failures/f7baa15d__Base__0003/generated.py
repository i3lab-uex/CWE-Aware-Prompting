import threading
from queue import Queue, Full

# Maximum number of tasks allowed in the queue to prevent resource exhaustion (CWE‑770 mitigation)
MAX_QUEUE_SIZE = 10000

# Global thread‑safe queue for tasks
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect modifications that might involve additional checks (optional)
_queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    task_id : str
        Unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise (e.g., queue full).
    """
    # Basic validation
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    try:
        # Queue.put_nowait will raise Full if the queue is at its maxsize
        task_queue.put_nowait((task_id, task_data))
        return True
    except Full:
        # Queue is full; refuse to accept new tasks
        return False