import threading
from queue import Queue, Full

# Global task queue with a configurable maximum size to prevent uncontrolled resource consumption.
MAX_QUEUE_SIZE = 1000  # Adjust based on system capacity and requirements
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# A lock to protect operations that need atomicity beyond the queue's own thread safety.
queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Adds a new task to the global task queue.

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

    # Attempt to put the task into the queue without blocking.
    try:
        with queue_lock:  # Ensure atomic check and put
            task_queue.put_nowait((task_id, task_data))
        return True
    except Full:
        # Queue is at capacity; do not add the task.
        return False
    except Exception:
        # Catch any unforeseen exception to avoid leaking resources or crashing.
        return False