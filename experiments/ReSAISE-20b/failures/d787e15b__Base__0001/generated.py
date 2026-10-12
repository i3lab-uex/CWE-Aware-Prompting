import queue
from typing import Dict

# Global task queue with a maximum size to mitigate CWE-770.
# Adjust MAX_QUEUE_SIZE according to system constraints.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task in the global `task_queue`.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Parameters or payload associated with the task.

    Returns
    -------
    bool
        True if the task was added to the queue, False otherwise (e.g., queue full).
    """
    # Ensure input validity
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Attempt to enqueue the task without blocking
    try:
        task_queue.put_nowait((task_reference, parameters))
        return True
    except queue.Full:
        # Queue reached its capacity; task cannot be added.
        return False
    except Exception:
        # Catch any unforeseen exceptions to keep the function robust
        return False