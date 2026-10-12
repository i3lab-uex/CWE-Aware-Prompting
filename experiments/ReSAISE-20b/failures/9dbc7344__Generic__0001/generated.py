import queue
from typing import Dict

# Global thread‑safe task queue.  Each item is a tuple (identifier, content).
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()


def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Enqueue a new task into the global `task_queue`.

    Parameters
    ----------
    task_identifier : str
        A unique identifier for the task.
    task_content : dict
        The payload/parameters of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    try:
        # Basic validation to avoid malformed entries
        if not isinstance(task_identifier, str) or not task_identifier:
            return False
        if not isinstance(task_content, dict):
            return False

        # Queue is thread‑safe; put_nowait will raise queue.Full if the
        # queue has a maxsize and is full.
        task_queue.put_nowait((task_identifier, task_content))
        return True
    except queue.Full:
        # Queue has reached its maximum size; caller can retry later.
        return False
    except Exception:
        # Any other unexpected error should not crash the caller.
        return False