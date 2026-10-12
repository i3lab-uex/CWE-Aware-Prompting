import threading
from queue import Queue, Full

# Global task queue with a reasonable maximum size to avoid resource exhaustion.
# Adjust `MAX_QUEUE_SIZE` as appropriate for the deployment environment.
MAX_QUEUE_SIZE = 10_000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect operations that need atomicity beyond the queue itself
_queue_lock = threading.Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing the task's parameters and specifics.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation: ensure the task ID is a non-empty string and
    # that task_info is a dictionary. Reject otherwise.
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Use the queue's built‑in thread safety; no additional lock is needed
    try:
        # Try to enqueue immediately; if the queue is full, we fail gracefully.
        task_queue.put_nowait((unique_task_id, task_info))
    except Full:
        # The queue has reached its maximum size; reject the new task.
        return False

    return True