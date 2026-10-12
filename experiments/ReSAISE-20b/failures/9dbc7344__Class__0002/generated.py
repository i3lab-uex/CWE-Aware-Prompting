import queue
from threading import Lock

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
MAX_QUEUE_SIZE = 10_000
_task_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# A lock to guard the check-and-enqueue operation when using a custom queue implementation.
# (Not strictly needed for `queue.Queue`, but harmless and future‑proof.)
_queue_lock = Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique identifier for the task.
    task_content : dict
        Parameters and specifics of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise (e.g., queue full).
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    # Compose the task tuple (identifier, content).  Using a tuple keeps the item immutable.
    task_item = (task_identifier, dict(task_content))

    # Attempt to enqueue with a non‑blocking put.  This avoids blocking threads and
    # allows us to return False if the queue is full.
    try:
        _task_queue.put(task_item, block=False)
        return True
    except queue.Full:
        # Queue is at capacity; do not enqueue to avoid uncontrolled resource consumption.
        return False
    except Exception:
        # Catch-all for unforeseen errors; do not propagate exceptions.
        return False