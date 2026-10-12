import queue
from typing import Dict

# Global task queue with a reasonable maximum size to avoid uncontrolled growth (CWE‑770 mitigation)
TASK_QUEUE_MAXSIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a task to the global queue in a thread‑safe manner.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        A dictionary containing parameters and metadata for the task.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise (e.g., queue full).

    Notes
    -----
    - The function attempts a non‑blocking enqueue to avoid deadlocks.
    - If the queue is at capacity, it returns False rather than blocking or raising.
    """
    try:
        # Use put_nowait to avoid blocking; will raise queue.Full if the limit is reached
        task_queue.put_nowait((identifier, details))
        return True
    except queue.Full:
        # Queue is full; task not enqueued
        return False