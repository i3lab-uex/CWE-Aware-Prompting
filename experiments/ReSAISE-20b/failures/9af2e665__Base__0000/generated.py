import multiprocessing
from typing import Dict

# Global task queue with a reasonable maximum size to mitigate CWE‑770.
MAX_QUEUE_SIZE = 1000
task_queue: multiprocessing.Queue = multiprocessing.Queue(maxsize=MAX_QUEUE_SIZE)

def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely push a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Prevent queue overflow; if full, do not block indefinitely
    try:
        task_queue.put_nowait((task_uid, task_info))
        return True
    except multiprocessing.queues.Full:
        # Queue is full; could implement throttling or logging here
        return False
    except Exception:
        # Catch any unforeseen exception to maintain API contract (no raise)
        return False