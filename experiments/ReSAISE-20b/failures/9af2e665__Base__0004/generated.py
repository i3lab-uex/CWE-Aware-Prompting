import threading
from queue import Queue, Full

# Global task queue instance.  In a real application this would be
# created once and shared across modules.
task_queue: Queue = Queue()

# Optional queue size limit to guard against CWE‑770
MAX_QUEUE_SIZE = 1000

def push_task_to_queue(task_uid: str, task_info: dict) -> bool:
    """
    Insert a new task into the global task queue.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information about the task.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Ensure we don't exceed the configured queue size.
    if task_queue.qsize() >= MAX_QUEUE_SIZE:
        # Queue is full; we reject the new task to avoid unbounded growth.
        return False

    try:
        # Use a tuple so that the queue stores both UID and data together.
        task_queue.put((task_uid, task_info), block=False)
    except Full:
        # Rare race condition where the queue became full after qsize() check.
        return False
    except Exception:
        # Catch-all for unexpected errors; do not propagate exceptions.
        return False

    return True