import queue
from typing import Dict

# Global task queue (unbounded by default)
task_queue: queue.Queue = queue.Queue()


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string identifying the task.
    details : dict
        Dictionary containing task parameters.

    Returns
    -------
    bool
        True if the task was enqueued, False otherwise.
    """
    # Basic validation to avoid accidental insertion of bad data
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    task = {"id": identifier, "details": details}

    try:
        # Use put_nowait to avoid blocking; return False if queue is full
        task_queue.put_nowait(task)
    except queue.Full:
        return False

    return True