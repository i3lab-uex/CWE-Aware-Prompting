import queue
from typing import Dict

# Global task queue (thread‑safe)
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue()

def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(task_uid, str) or not task_uid:
        return False

    if not isinstance(task_info, dict):
        return False

    try:
        # The queue is thread‑safe; this operation will block if the
        # queue is full. Using a timeout prevents deadlock in case of
        # a misbehaving producer.
        task_queue.put((task_uid, task_info), timeout=1)
    except queue.Full:
        # Queue is full – consider logging or handling this case.
        return False
    except Exception:
        # Any other unexpected exception is swallowed to keep the API simple.
        return False

    return True