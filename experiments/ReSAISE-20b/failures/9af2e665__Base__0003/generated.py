import multiprocessing
from typing import Dict

# Global task queue (configured with a reasonable maxsize to mitigate CWE‑770)
TASK_QUEUE_MAXSIZE = 1000
task_queue: multiprocessing.Queue[str] = multiprocessing.Queue(maxsize=TASK_QUEUE_MAXSIZE)


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely push a new task into the global task queue.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Ensure the queue is not full to avoid uncontrolled growth
    if task_queue.full():
        return False

    try:
        # Put the task into the queue without blocking
        task_queue.put_nowait((task_uid, task_info))
    except (multiprocessing.queues.Full, Exception):
        # Any exception during put is treated as a failure
        return False

    return True