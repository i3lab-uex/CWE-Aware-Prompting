import queue
from typing import Dict

# Global task queue – thread‑safe FIFO queue with unlimited size
task_queue: queue.Queue = queue.Queue()

def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        The payload containing task specifics and parameters.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation – avoid inserting None or empty identifiers
    if not task_identifier or not isinstance(task_content, dict):
        return False

    # Construct the task tuple (identifier, content)
    task = (task_identifier, task_content)

    try:
        # Non‑blocking put; will raise queue.Full if the queue is bounded
        task_queue.put_nowait(task)
    except Exception:
        # Any exception (e.g., Full) results in a failure flag
        return False

    return True