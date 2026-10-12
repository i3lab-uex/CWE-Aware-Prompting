import queue
from typing import Dict

# Global task queue (should be defined elsewhere in the application).
# Here we provide a default with an explicit size limit to mitigate
# CWE‑770 (unbounded resource allocation).
try:
    task_queue  # type: ignore
except NameError:
    # If the global queue is not defined, create one with a sensible limit.
    task_queue = queue.Queue(maxsize=1000)  # Adjust the size as appropriate for your environment.

def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Safely enqueue a task into the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Parameters and metadata associated with the task.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Validate inputs
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    task = {"id": identifier, "details": details}

    try:
        # Use a non-blocking put to avoid hanging the caller.
        task_queue.put_nowait(task)
    except queue.Full:
        # Queue reached its capacity; reject the task.
        return False
    except Exception:
        # Unexpected error – treat as failure to enqueue.
        return False

    return True