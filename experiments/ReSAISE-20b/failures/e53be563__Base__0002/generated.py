import queue
from typing import Dict

# Global task queue; in a real system this would be configured elsewhere.
# Using a bounded queue to mitigate CWE-770 by limiting the maximum number of tasks.
TASK_QUEUE_MAXSIZE = 10000
task_queue: queue.Queue[str] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)


def push_task(uid: str, data: Dict) -> bool:
    """
    Attempt to add a task identified by `uid` with associated `data`
    into the global `task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Task payload.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    # Ensure we don't exceed the queue capacity
    if task_queue.full():
        # Queue is at capacity; reject new tasks to avoid unbounded growth.
        return False

    try:
        # Store a tuple of (uid, data) for later processing
        task_queue.put_nowait((uid, data))
    except queue.Full:
        # Race condition: another thread filled the queue between full() check and put_nowait()
        return False
    except Exception:
        # Catch-all to prevent any unexpected exception from propagating
        return False

    return True