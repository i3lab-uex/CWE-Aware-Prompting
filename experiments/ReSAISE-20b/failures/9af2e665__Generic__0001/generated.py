import queue
from typing import Dict, Any

# Global task queue (should be initialized elsewhere in the system)
task_queue: "queue.Queue[tuple[str, Dict[str, Any]]]" = queue.Queue()


def push_task_to_queue(task_uid: str, task_info: Dict[str, Any]) -> bool:
    """
    Insert a new task into the global task queue.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_uid, str):
        return False
    if not isinstance(task_info, dict):
        return False

    try:
        # The queue holds a tuple of (task_uid, task_info)
        task_queue.put_nowait((task_uid, task_info))
    except queue.Full:
        # Queue is full – cannot add new tasks
        return False
    except Exception:
        # Catch any unexpected exception to avoid propagating errors
        return False

    return True