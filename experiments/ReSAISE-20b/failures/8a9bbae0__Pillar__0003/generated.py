import queue
import threading

# Global task queue and a set to track unique identifiers.
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=1000)
# Protects access to the identifier set.
_id_lock = threading.Lock()
_task_ids: set[str] = set()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_details : dict
        A dictionary encompassing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task is successfully enqueued, False otherwise.
    """
    # Validate inputs
    if not isinstance(task_identifier, str):
        return False
    if not isinstance(task_details, dict):
        return False

    # Ensure the task identifier is unique.
    with _id_lock:
        if task_identifier in _task_ids:
            return False
        # Reserve the identifier before attempting to enqueue.
        _task_ids.add(task_identifier)

    try:
        # Attempt to enqueue without blocking. If the queue is full, we
        # treat it as a failure and remove the reserved identifier.
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        with _id_lock:
            _task_ids.discard(task_identifier)
        return False

    # Success
    return True