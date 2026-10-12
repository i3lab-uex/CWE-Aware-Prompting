import queue
import threading

# Global task queue with a bounded size to mitigate uncontrolled resource consumption (CWE-400)
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Global set to keep track of enqueued task identifiers and ensure uniqueness
_enqueued_ids: set[str] = set()
_id_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue for subsequent processing.

    Args:
        task_identifier (str): A unique string identifier assigned to each task.
        task_details (dict): A dictionary encompassing the task's specifics and parameters.

    Returns:
        bool: True if the task is successfully enqueued, False otherwise.
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    # Ensure the task identifier is unique
    with _id_lock:
        if task_identifier in _enqueued_ids:
            return False  # Duplicate identifier

    try:
        # Attempt to enqueue without blocking; will raise queue.Full if the queue is full
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        return False

    # Register the identifier after successful enqueue
    with _id_lock:
        _enqueued_ids.add(task_identifier)

    return True