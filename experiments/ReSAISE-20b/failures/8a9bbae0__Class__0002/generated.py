import queue
from typing import Dict

# Global task queue with a maximum size to mitigate uncontrolled resource consumption.
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_details : dict
        Dictionary containing task-specific parameters.

    Returns
    -------
    bool
        True if the task was enqueued, False otherwise (e.g., queue full).
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    try:
        # Non-blocking put; if the queue is full, this will raise Full.
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue is at capacity; cannot accept more tasks.
        return False

    return True