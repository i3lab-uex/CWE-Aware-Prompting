import queue
from typing import Dict, Any

# Global task queue with a configurable maximum size to avoid resource exhaustion
MAX_QUEUE_SIZE = 10_000          # Adjust as needed for your environment
task_queue: queue.Queue[tuple[str, Dict[str, Any]]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(task_identifier: str, task_details: Dict[str, Any]) -> bool:
    """
    Add a new task to the global queue.

    Args:
        task_identifier (str): A unique string identifier for the task.
        task_details (dict): Dictionary containing task parameters.

    Returns:
        bool: True if the task was enqueued, False if the queue is full.
    """
    try:
        # Attempt to enqueue without blocking. If the queue is full, a Full exception is raised.
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue has reached its maximum size; cannot enqueue the new task.
        return False
    return True