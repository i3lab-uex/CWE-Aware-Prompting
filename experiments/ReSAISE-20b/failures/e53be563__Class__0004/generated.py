import queue
from typing import Dict

# Global task queue with a limited size to prevent uncontrolled resource consumption.
# The maxsize can be tuned according to system capacity. 0 means unlimited, so we set a
# reasonable default (e.g., 1000 tasks) to guard against exhaustion.
TASK_QUEUE_MAXSIZE = 1000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)


def push_task(uid: str, data: Dict) -> bool:
    """
    Safely add a task to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Dictionary containing task parameters.

    Returns
    -------
    bool
        True if the task was enqueued, False if the queue is full.
    """
    # Quick validation of inputs
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    try:
        # queue.put_nowait raises queue.Full if the queue is at capacity.
        task_queue.put_nowait((uid, data))
        return True
    except queue.Full:
        # Queue is full; cannot accept more tasks at this time.
        return False