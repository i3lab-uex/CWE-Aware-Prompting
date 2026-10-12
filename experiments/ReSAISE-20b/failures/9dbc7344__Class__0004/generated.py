import queue
import threading

# Global task queue with a limited size to avoid uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to system capacity requirements.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Global set to track already queued task identifiers.
# Protect access with a lock for thread safety.
_task_ids = set()
_task_ids_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue for subsequent processing.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_content : dict
        A dictionary encompassing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task is successfully enqueued, False otherwise.
    """
    # Basic validation: ensure inputs are of expected types
    if not isinstance(task_identifier, str) or not isinstance(task_content, dict):
        return False

    # Check for duplicate identifiers to prevent accidental re-queueing
    with _task_ids_lock:
        if task_identifier in _task_ids:
            return False

    # Attempt to enqueue the task without blocking
    try:
        task_queue.put_nowait((task_identifier, task_content))
    except queue.Full:
        # Queue is at capacity; do not block or raise
        return False

    # Mark the identifier as queued
    with _task_ids_lock:
        _task_ids.add(task_identifier)

    return True