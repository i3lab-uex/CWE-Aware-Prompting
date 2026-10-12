import queue
from typing import Dict

# Define a maximum size for the global task queue to mitigate CWE‑770
MAX_QUEUE_SIZE = 10_000

# Global, thread‑safe queue for tasks
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that serves as an identifier for each task.
    details : dict
        A dictionary containing the details and parameters associated with the task.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    try:
        # Try to enqueue without blocking; if full, this raises queue.Full
        task_queue.put_nowait((identifier, details))
        return True
    except queue.Full:
        # Queue is at capacity; do not block or raise an exception
        return False