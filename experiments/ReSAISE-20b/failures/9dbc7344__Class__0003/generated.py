import threading
from queue import Queue, Full

# Global task queue with a sensible maximum size to prevent uncontrolled resource consumption.
TASK_QUEUE_MAXSIZE = 10_000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=TASK_QUEUE_MAXSIZE)

# A lock to protect any additional consistency checks if needed.
queue_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue for later processing.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_content : dict
        Dictionary containing the specifics and parameters of the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation: ensure arguments are of expected types
    if not isinstance(task_identifier, str) or not isinstance(task_content, dict):
        return False

    # Use a lock to avoid race conditions when checking and putting.
    with queue_lock:
        try:
            # Attempt a non-blocking put; this raises Full if the queue is at capacity.
            task_queue.put_nowait((task_identifier, task_content))
        except Full:
            # Queue is full; refuse to enqueue to avoid uncontrolled resource consumption.
            return False
        except Exception:
            # Any other exception is considered a failure to enqueue.
            return False

    return True