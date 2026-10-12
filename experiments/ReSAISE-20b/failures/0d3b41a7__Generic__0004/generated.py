import threading
from queue import Queue, Full

# Global task queue (FIFO) with a reasonable maxsize to prevent memory exhaustion.
# Adjust `maxsize` as needed for your application; 0 means infinite.
task_queue: Queue = Queue(maxsize=1000)

# A lock to protect the task queue and any auxiliary structures.
_queue_lock = threading.Lock()

# Optional: keep track of task IDs to prevent duplicates.
_enqueued_ids = set()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Safely enqueue a new task into the global `task_queue`.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task. Duplicate IDs are rejected.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    with _queue_lock:
        # Reject duplicate task IDs
        if unique_task_id in _enqueued_ids:
            return False

        try:
            # Attempt to enqueue the task. If the queue is full, Full exception will be raised.
            task_queue.put_nowait((unique_task_id, task_info))
        except Full:
            # Queue is full; cannot enqueue the task.
            return False

        # Record that this ID has been enqueued
        _enqueued_ids.add(unique_task_id)

    return True