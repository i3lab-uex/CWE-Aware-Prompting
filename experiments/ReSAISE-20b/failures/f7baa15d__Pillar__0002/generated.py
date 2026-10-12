import queue
from typing import Dict

# Global thread‑safe queue for tasks
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # adjust maxsize as needed


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Adds a new task to the global task_queue.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False otherwise (e.g., when the queue is full).
    """
    if not isinstance(task_id, str) or not isinstance(task_data, dict):
        # Invalid input types; do not add to queue
        return False

    try:
        # Use put_nowait to avoid blocking; if the queue is full, catch exception
        task_queue.put_nowait((task_id, task_data))
    except queue.Full:
        # Queue has reached its maximum capacity
        return False

    return True