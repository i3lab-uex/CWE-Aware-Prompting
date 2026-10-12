import queue
from threading import Lock

# Global task queue with a maximum size to mitigate CWE‑770.
MAX_QUEUE_SIZE = 1000   # Adjust as appropriate for your environment
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Keeps track of task IDs already enqueued to enforce uniqueness.
_enqueued_ids = set()
_id_lock = Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue.

    Args:
        unique_task_id: A unique string identifier for the task.
        task_info: Dictionary containing task parameters.

    Returns:
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(unique_task_id, str) or not isinstance(task_info, dict):
        return False

    # Ensure the task ID is unique
    with _id_lock:
        if unique_task_id in _enqueued_ids:
            return False
        # Reserve the ID before attempting to enqueue
        _enqueued_ids.add(unique_task_id)

    try:
        # Attempt to add the task without blocking
        task_queue.put_nowait((unique_task_id, task_info))
    except queue.Full:
        # Queue is full; release the reserved ID
        with _id_lock:
            _enqueued_ids.remove(unique_task_id)
        return False

    # Task successfully enqueued
    return True