import queue
from typing import Dict

# Global task queue used by the system.
# A maxsize is set to prevent unbounded growth (CWE‑770 mitigation).
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Ensure we don't exceed the maximum queue size
    if task_queue.full():
        return False

    try:
        # Use a tuple to keep the unique_id separate from the task payload
        task_queue.put_nowait((unique_id, task_info))
    except queue.Full:
        # Rare race condition where the queue became full between checks
        return False
    except Exception:
        # Any unexpected exception should not crash the system; log if needed.
        return False

    return True