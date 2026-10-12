import threading
from queue import Queue, Full

# Global task queue with a maximum size to prevent resource exhaustion.
# Adjust MAX_QUEUE_SIZE according to system requirements.
MAX_QUEUE_SIZE = 1000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect concurrent access when checking the queue size.
_queue_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Args:
        task_identifier (str): Unique identifier for the task.
        task_details (dict): Dictionary containing task specifics and parameters.

    Returns:
        bool: True if the task was enqueued successfully, False otherwise.
    """
    # Validate inputs
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    # Attempt to enqueue with a timeout to avoid blocking indefinitely.
    try:
        task_queue.put((task_identifier, task_details), block=False)
        return True
    except Full:
        # Queue is full; do not enqueue to avoid uncontrolled resource growth.
        return False