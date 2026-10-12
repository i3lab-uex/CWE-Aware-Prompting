import queue
from typing import Dict

# Global task queue. In a real system this would be instantiated elsewhere.
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # limit to avoid unlimited growth

def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely add a new task to the global `task_queue`.

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
    # Ensure required fields are present
    if not isinstance(task_uid, str) or not task_uid:
        return False

    if not isinstance(task_info, dict):
        return False

    # Avoid overfilling the queue (CWE-770 mitigation)
    try:
        if task_queue.full():
            # Queue is at capacity; reject new tasks
            return False

        # Wrap task data into a tuple to preserve UID and info
        task_entry = (task_uid, task_info)
        task_queue.put_nowait(task_entry)
    except queue.Full:
        # Another thread filled the queue between full() check and put_nowait()
        return False
    except Exception:
        # Unexpected error; do not propagate to caller
        return False

    return True