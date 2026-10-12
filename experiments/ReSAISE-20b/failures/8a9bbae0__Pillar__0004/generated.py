import queue
from typing import Dict

# Global thread‑safe task queue
task_queue: "queue.Queue[tuple[str, dict]]" = queue.Queue()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        Dictionary containing parameters and specifics of the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic type validation
    if not isinstance(task_identifier, str):
        return False
    if not isinstance(task_details, dict):
        return False

    try:
        # The queue is thread‑safe; put_nowait will raise if the queue is full.
        task_queue.put_nowait((task_identifier, task_details))
    except Exception:
        # Any exception (e.g., full queue) results in a failed enqueue.
        return False

    return True