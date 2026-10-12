import threading
from queue import Queue, Full

# Global task queue used by the multi‑threaded system.
# Initialized with a reasonable maximum size to avoid unbounded growth
# and potential resource exhaustion (CWE‑664 consideration).
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=1000)

# Lock to protect the global task_queue during insertion
_task_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        Dictionary containing the specifics and parameters of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic input validation to avoid malformed entries
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_content, dict):
        return False

    # Ensure the task tuple is hashable and immutable for safety
    try:
        task_item = (task_identifier, dict(task_content))
    except Exception:
        return False

    # Enqueue the task in a thread‑safe manner
    try:
        with _task_lock:
            # Queue.put_nowait raises Full if the queue is at maxsize
            task_queue.put_nowait(task_item)
        return True
    except Full:
        # Queue is full; the task cannot be enqueued at this time.
        return False
    except Exception:
        # Any other unexpected exception is treated as a failure to enqueue.
        return False