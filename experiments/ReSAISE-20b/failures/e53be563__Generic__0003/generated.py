import queue
from typing import Dict

# Global task queue (created if it does not already exist)
try:
    # If the global variable has been defined elsewhere, use it
    task_queue  # noqa: F821
except NameError:
    task_queue = queue.Queue(maxsize=0)  # unlimited size


def push_task(uid: str, data: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Task parameters and payload.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    task_item = {"uid": uid, "data": data}

    try:
        # queue.Queue is thread‑safe; put_nowait raises Full if a maxsize is set
        task_queue.put_nowait(task_item)
    except queue.Full:
        # Queue is full (unlikely with unlimited size)
        return False
    except Exception:
        # Catch any unexpected error to avoid propagating exceptions
        return False

    return True