import queue
from typing import Dict

# Global task queue used by the parallel processing system.
task_queue: queue.Queue = queue.Queue()

def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid corrupt entries
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    try:
        # Use a small timeout to avoid blocking indefinitely.
        task_queue.put((unique_id, task_info), block=False)
    except queue.Full:
        # Queue is full; consider logging here in a real system.
        return False
    except Exception:
        # Catch any unexpected exception silently as per spec (no raise).
        return False

    return True