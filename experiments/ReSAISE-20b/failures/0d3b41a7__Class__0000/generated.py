import threading
from queue import Queue, Full

# Maximum number of tasks that can be queued at once.
MAX_QUEUE_SIZE = 1000

# Global task queue and a set to keep track of unique task IDs.
_task_queue: Queue = Queue(maxsize=MAX_QUEUE_SIZE)
_task_ids: set[str] = set()
_lock = threading.Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier assigned to each task.
    task_info : dict
        A dictionary encompassing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task is successfully enqueued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    with _lock:
        # Prevent duplicate task IDs
        if unique_task_id in _task_ids:
            return False

        # Attempt to enqueue the task
        try:
            _task_queue.put((unique_task_id, task_info), block=False)
        except Full:
            # Queue is full; cannot accept more tasks
            return False

        # Register the task ID so it can't be queued again
        _task_ids.add(unique_task_id)
    return True


# Optional helper to dequeue tasks (for completeness)
def get_next_task():
    """
    Retrieve the next task from the queue.
    This function blocks until a task is available.

    Returns
    -------
    tuple[str, dict]
        The unique_task_id and task_info of the next queued task.
    """
    unique_task_id, task_info = _task_queue.get()
    with _lock:
        # Remove the ID from the set once it has been dequeued
        _task_ids.discard(unique_task_id)
    return unique_task_id, task_info