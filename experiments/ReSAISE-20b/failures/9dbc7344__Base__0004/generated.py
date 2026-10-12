import threading
from queue import Queue, Full

# Global task queue with a maximum size to prevent resource exhaustion (CWE‑770 mitigation).
MAX_QUEUE_SIZE = 10_000          # Adjust as appropriate for your environment
_task_queue_lock = threading.Lock()
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Safely enqueue a new task into the global `task_queue`.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        The task's parameters and data.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    try:
        # Use a lock to ensure thread‑safety for the enqueue operation
        with _task_queue_lock:
            task_queue.put((task_identifier, task_content), block=False)
        return True
    except Full:
        # Queue is full; reject the task to avoid unlimited growth
        return False
    except Exception:
        # Any unexpected exception is swallowed to keep the API simple
        return False