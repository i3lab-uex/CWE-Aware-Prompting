import threading
from queue import Queue, Full

# Global task queue with a maximum size to avoid uncontrolled growth (CWE-770 mitigation)
_MAX_QUEUE_SIZE = 1000  # adjust as needed for your system
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=_MAX_QUEUE_SIZE)

# Lock to ensure atomicity when checking the queue size and adding a task
_queue_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_details : dict
        A dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    # Attempt to enqueue the task with a timeout of 0 seconds to avoid blocking
    try:
        # Using put_nowait ensures we don't block if the queue is full.
        task_queue.put_nowait((task_identifier, task_details))
        return True
    except Full:
        # Queue is full; do not enqueue the task.
        return False