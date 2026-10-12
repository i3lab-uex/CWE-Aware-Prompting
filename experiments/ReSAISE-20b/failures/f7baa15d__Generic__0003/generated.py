import threading
from collections import deque
from typing import Dict

# Global task queue and a set to track existing task IDs for uniqueness checks
_task_queue: deque = deque()
_existing_ids: set[str] = set()

# Lock to synchronize access to the queue and ID set
_queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Add a new task to the global queue in a thread‑safe manner.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_id, str) or not task_id:
        return False

    if not isinstance(task_data, dict):
        return False

    with _queue_lock:
        # Ensure task_id uniqueness
        if task_id in _existing_ids:
            return False

        # Append the new task as a tuple (task_id, task_data)
        _task_queue.append((task_id, task_data))
        _existing_ids.add(task_id)

    return True