import queue
from typing import Dict

# Global task queue with a bounded size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE as appropriate for your environment.
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_details : dict
        A dictionary encompassing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Validate input types
    if not isinstance(task_identifier, str) or not isinstance(task_details, dict):
        return False

    # Attempt to enqueue without blocking; fail gracefully if the queue is full.
    try:
        task_queue.put_nowait((task_identifier, task_details))
        return True
    except queue.Full:
        # The queue has reached its maximum capacity; task is not enqueued.
        return False