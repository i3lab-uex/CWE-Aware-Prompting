import threading
from queue import Queue, Full

# Maximum number of tasks that can be queued at once to avoid uncontrolled resource consumption.
MAX_QUEUE_SIZE = 10_000

# Global task queue (thread‑safe).
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect checks that involve both the queue size and task addition.
enqueue_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Args:
        task_identifier: Unique string identifier for the task.
        task_details: Dictionary containing parameters specific to the task.

    Returns:
        True if the task was enqueued successfully; False otherwise (e.g., queue full).

    Raises:
        None
    """
    # Validate input types early.
    if not isinstance(task_identifier, str):
        raise TypeError("task_identifier must be a string")
    if not isinstance(task_details, dict):
        raise TypeError("task_details must be a dictionary")

    # Attempt to enqueue without blocking. If the queue is full, return False.
    try:
        with enqueue_lock:  # Ensure atomicity for size check and put_nowait
            if task_queue.full():
                return False
            # Put the task into the queue. This will not block because we checked full().
            task_queue.put_nowait((task_identifier, task_details))
    except Full:
        # This should not happen due to the check above but handle it defensively.
        return False

    return True