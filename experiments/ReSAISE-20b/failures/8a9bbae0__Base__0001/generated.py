import threading
from queue import Queue, Full

# Maximum number of tasks allowed in the queue to mitigate CWE-770
MAX_QUEUE_SIZE = 10_000

# Global task queue with a size limit and thread‑safety
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to guard operations that need atomicity beyond the queue itself
_queue_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique identifier for the task.
    task_details : dict
        Parameters and specifics of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate inputs quickly
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    # Use the queue's built‑in thread safety and size limit
    try:
        with _queue_lock:  # Ensure atomic check‑and‑add if needed
            task_queue.put_nowait((task_identifier, task_details))
        return True
    except Full:
        # Queue is full; we refuse to accept more tasks
        return False
    except Exception:
        # Any unexpected error is swallowed; operation fails gracefully
        return False