import queue
from threading import Lock

# Global task queue and a lock to protect it.
task_queue = queue.Queue()
_task_ids = set()  # Tracks IDs that have already been queued
_task_lock = Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and specifics.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False

    if not isinstance(task_info, dict):
        return False

    # Prevent duplicate task IDs
    with _task_lock:
        if unique_task_id in _task_ids:
            return False

        # Enqueue the task
        try:
            task_queue.put_nowait((unique_task_id, task_info))
        except queue.Full:
            return False

        # Record the ID to avoid future duplicates
        _task_ids.add(unique_task_id)

    return True