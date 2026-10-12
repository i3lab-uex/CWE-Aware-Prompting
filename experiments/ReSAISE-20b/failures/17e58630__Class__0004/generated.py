import threading
from queue import Queue, Full

# Global task queue with a sensible maximum size to avoid uncontrolled resource consumption.
MAX_QUEUE_SIZE = 1000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect any additional shared state if needed in the future.
_queue_lock = threading.Lock()


def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Dictionary containing parameters and metadata for the task.

    Returns
    -------
    bool
        True if the task was added to the queue, False otherwise.
    """
    # Basic validation: ensure identifier is a non-empty string and details is a dict.
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    # Attempt to enqueue the task without blocking.
    try:
        with _queue_lock:  # optional, but protects future extensions
            task_queue.put_nowait((identifier, details))
        return True
    except Full:
        # Queue is full; do not block or raise an exception.
        return False