import threading
from queue import Queue, Full

# Global task queue shared across threads.
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=1000)

# Optional lock for protecting auxiliary structures (e.g., tracking IDs).
queue_lock = threading.Lock()


def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Safely add a new task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Validate inputs to avoid malformed tasks.
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    try:
        # Acquire a lock only for operations that need to be atomic
        with queue_lock:
            task_queue.put_nowait((identifier, details))
    except Full:
        # Queue capacity reached; cannot enqueue.
        return False
    except Exception:
        # Catch unexpected exceptions to avoid leaking resources.
        return False

    return True