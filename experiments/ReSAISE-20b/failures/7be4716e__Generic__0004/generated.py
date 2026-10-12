# enqueue_task.py

import queue
from typing import Dict, Any

# Global task queue – in a real application this would be initialized elsewhere
task_queue: queue.Queue = queue.Queue(maxsize=1000)


def enqueue_task(unique_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    unique_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing the task's details, parameters, etc.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid corrupting the queue
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Create a lightweight container for the task
    task_payload = {"id": unique_id, "info": task_info}

    try:
        # Use non-blocking put to avoid hanging the caller
        task_queue.put_nowait(task_payload)
    except queue.Full:
        # Queue is full – cannot enqueue the task
        return False
    except Exception:
        # Catch any unexpected error to keep the function from raising
        return False

    return True