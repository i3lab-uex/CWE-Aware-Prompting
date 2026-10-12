import queue
from typing import Dict

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to system capacity.
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global queue.

    Args:
        unique_task_id (str): A unique identifier for the task.
        task_info (Dict): Dictionary containing task parameters.

    Returns:
        bool: True if the task was enqueued, False if the queue is full.
    """
    # Validate input types
    if not isinstance(unique_task_id, str) or not isinstance(task_info, dict):
        return False

    # Attempt to enqueue without blocking; if the queue is full, return False
    try:
        task_queue.put_nowait((unique_task_id, task_info))
        return True
    except queue.Full:
        # Queue is full; do not block to avoid resource exhaustion
        return False