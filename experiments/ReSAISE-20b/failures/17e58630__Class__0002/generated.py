import queue
from typing import Dict

# Global task queue with a bounded size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to system constraints.
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Parameters and data required to execute the task.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic validation: ensure identifier is a non-empty string
    if not isinstance(identifier, str) or not identifier.strip():
        return False

    # Ensure details is a dictionary
    if not isinstance(details, dict):
        return False

    try:
        # Try to put the task into the queue without blocking.
        task_queue.put_nowait((identifier, details))
    except queue.Full:
        # Queue is at capacity; do not block to avoid resource exhaustion.
        return False

    return True