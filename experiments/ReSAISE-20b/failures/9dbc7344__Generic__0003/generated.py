import queue
from typing import Dict

# Global thread‑safe queue for task storage.
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()

def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_content : dict
        Dictionary containing the task parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_content, dict):
        return False

    try:
        # Enqueue the task as a tuple (identifier, content)
        task_queue.put_nowait((task_identifier, task_content))
    except queue.Full:
        # Queue is full; operation failed
        return False
    except Exception:
        # Unexpected error – be conservative and signal failure
        return False

    return True