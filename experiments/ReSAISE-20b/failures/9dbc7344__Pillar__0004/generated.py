import queue
from typing import Dict

# Global task queue used by the system.
# Initialized lazily to avoid side‑effects at import time.
_task_queue: queue.Queue | None = None


def _get_task_queue() -> queue.Queue:
    """Return the singleton task queue, creating it if necessary."""
    global _task_queue
    if _task_queue is None:
        # Use a FIFO queue with unlimited size.  In real systems you might
        # configure maxsize or use a different data structure.
        _task_queue = queue.Queue()
    return _task_queue


def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue for processing.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_content : dict
        A dictionary encompassing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    try:
        # Ensure that we are working with the correct queue instance
        q = _get_task_queue()
        # Enqueue a tuple containing identifier and content.
        # Using put_nowait() to avoid blocking; we return False if the
        # queue is full (unlikely with an unbounded Queue).
        q.put_nowait((task_identifier, task_content))
    except queue.Full:
        # The queue is full; treat as a failure to enqueue.
        return False
    except Exception:
        # Any other exception (e.g., invalid arguments) is swallowed
        # and reported as a failure to preserve the contract of not raising.
        return False

    return True