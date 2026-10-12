import queue
from typing import Dict

# Global task queue used by the parallel processing system.
task_queue: queue.Queue = queue.Queue(maxsize=0)  # unbounded by default


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely insert a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Ensure inputs are of correct type; silently ignore incorrect types
    if not isinstance(task_uid, str) or not isinstance(task_info, dict):
        return False

    # Prepare the payload for queue insertion
    task_payload = {"uid": task_uid, "info": task_info}

    try:
        # Use put_nowait to avoid blocking; this will raise queue.Full if the
        # queue is bounded and full.
        task_queue.put_nowait(task_payload)
    except queue.Full:
        # Queue capacity exceeded (if bounded). No task added.
        return False
    except Exception:
        # Catch any unforeseen exception to prevent propagation.
        return False

    return True