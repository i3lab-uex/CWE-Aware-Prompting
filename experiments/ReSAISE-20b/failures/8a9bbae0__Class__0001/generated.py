import queue
from typing import Dict

# Global task queue with a bounded size to prevent uncontrolled resource consumption.
# The maximum number of tasks that can be queued at once is 10_000 by default. Adjust as needed.
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=10_000)

def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier assigned to each task.
    task_details : dict
        Dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise (e.g., queue is full).
    """
    try:
        # Use put_nowait to avoid blocking if the queue is at capacity.
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue is full; do not block. Caller can decide to retry later.
        return False
    except Exception:
        # Unexpected errors are not expected; propagate them to caller.
        raise
    return True