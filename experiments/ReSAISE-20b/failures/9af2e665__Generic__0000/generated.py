import queue
from typing import Dict

# Global task queue.  If the module is imported multiple times,
# we ensure that only one instance exists.
try:
    task_queue  # type: ignore[assignment]
except NameError:
    task_queue = queue.Queue()

def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Push a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information about the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Create a composite task entry
    task_entry = {
        "uid": task_uid,
        "info": task_info,
    }

    try:
        # Non-blocking put; if the queue is full, return False
        task_queue.put_nowait(task_entry)
    except queue.Full:
        # Queue is full; we could log or handle this case
        return False
    except Exception:
        # Catch any other unforeseen exceptions
        return False

    return True