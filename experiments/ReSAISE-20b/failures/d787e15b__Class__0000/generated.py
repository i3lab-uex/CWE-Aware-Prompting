import threading
from collections import deque
from typing import Dict

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
_MAX_QUEUE_SIZE = 1000
_task_queue: deque[tuple[str, Dict]] = deque(maxlen=_MAX_QUEUE_SIZE)
_queue_lock = threading.Lock()

def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Parameters associated with the task.

    Returns
    -------
    bool
        True if the task was added, False otherwise (duplicate or queue full).
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    with _queue_lock:
        # Prevent duplicate task references
        if any(ref == task_reference for ref, _ in _task_queue):
            return False

        # Respect the maximum queue size
        if len(_task_queue) >= _MAX_QUEUE_SIZE:
            return False

        # Append the new task
        _task_queue.append((task_reference, parameters))
    return True