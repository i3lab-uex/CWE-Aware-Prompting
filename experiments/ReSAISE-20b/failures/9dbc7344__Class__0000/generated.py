import queue
from threading import Lock

# Global task queue with a reasonable maximum size to mitigate CWE‑400.
MAX_QUEUE_SIZE = 10_000
task_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to serialize access when checking size and putting a task.
_queue_lock = Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique string identifier for the task.
    task_content : dict
        Dictionary containing task parameters and details.

    Returns
    -------
    bool
        True if the task was enqueued, False if the queue is full.
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    with _queue_lock:
        # Check if the queue is full before attempting to enqueue
        if task_queue.full():
            return False

        # Enqueue the task as a tuple (identifier, content)
        try:
            task_queue.put_nowait((task_identifier, task_content))
            return True
        except queue.Full:
            # Rare race condition: the queue became full after the check
            return False