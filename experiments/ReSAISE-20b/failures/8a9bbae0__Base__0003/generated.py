import threading
from queue import Queue, Full

# Global task queue with a reasonable upper bound to mitigate CWE‑770
_MAX_QUEUE_SIZE = 10_000          # Adjust as appropriate for the application
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=_MAX_QUEUE_SIZE)

def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        Dictionary containing task specifics and parameters.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    try:
        # Attempt to enqueue without blocking; if the queue is full, return False
        task_queue.put_nowait((task_identifier, task_details))
        return True
    except Full:
        # Queue is full; do not block or raise an exception
        return False