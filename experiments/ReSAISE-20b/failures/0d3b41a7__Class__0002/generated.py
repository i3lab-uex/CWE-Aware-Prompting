import threading
from queue import Queue, Full

# Global task queue with a maximum size to mitigate uncontrolled resource consumption (CWE-400).
MAX_QUEUE_SIZE = 1000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect any additional shared state if needed in the future.
_queue_lock = threading.Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue for subsequent processing.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier assigned to each task.
    task_info : dict
        Dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued; False otherwise.

    Notes
    -----
    - The function uses a bounded queue to prevent uncontrolled growth of the task list.
    - It attempts to enqueue without blocking; if the queue is full it returns False.
    """
    # Basic validation: ensure unique_task_id is a string and task_info is a dict.
    if not isinstance(unique_task_id, str) or not isinstance(task_info, dict):
        return False

    try:
        # Attempt to enqueue without blocking.
        task_queue.put((unique_task_id, task_info), block=False)
    except Full:
        # Queue is full; cannot enqueue new tasks at this time.
        return False
    except Exception:
        # Catch-all for unexpected errors (unlikely but safe).
        return False

    return True