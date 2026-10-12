import queue
from typing import Dict

# Global task queue with a sensible size limit to mitigate CWE-770.
# Adjust MAX_QUEUE_SIZE as needed for your environment.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        Dictionary containing the task's parameters and details.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(task_identifier, str) or not isinstance(task_content, dict):
        return False

    try:
        # put_nowait will raise queue.Full if the queue has reached its maxsize
        task_queue.put_nowait((task_identifier, task_content))
    except queue.Full:
        # Queue is full – cannot accept more tasks at this time
        return False

    return True