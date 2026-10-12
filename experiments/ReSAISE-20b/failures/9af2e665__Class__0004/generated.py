import queue
from typing import Dict

# Global task queue with a reasonable maximum size to avoid uncontrolled resource consumption.
TASK_QUEUE_MAXSIZE = 1000
task_queue: queue.Queue[str] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely add a new task to the global task queue.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task details.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Quick sanity checks to avoid unnecessary queue operations
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Ensure the queue is not full before attempting to enqueue.
    if task_queue.full():
        return False

    # Use put_nowait() to avoid blocking; handle any potential queue.Full exception
    try:
        task_queue.put_nowait((task_uid, task_info))
        return True
    except queue.Full:
        # Queue became full between the check and put_nowait
        return False