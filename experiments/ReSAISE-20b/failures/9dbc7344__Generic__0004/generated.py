import queue
from typing import Dict

# Global thread‑safe queue for tasks
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue()

def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global `task_queue`.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        Dictionary containing the specifics and parameters of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation to avoid accidental misuse
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    try:
        # Put the task into the queue without blocking
        task_queue.put_nowait((task_identifier, task_content))
    except queue.Full:
        # Queue capacity exceeded (unlikely with default unbounded queue)
        return False
    except Exception:
        # Any other unforeseen exception should not propagate
        return False

    return True