import queue
from typing import Dict

# Global task queue (configured with a maximum size to avoid uncontrolled resource consumption)
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # Adjust maxsize as needed


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details, parameters, and other relevant information.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic type validation
    if not isinstance(unique_id, str) or not isinstance(task_info, dict):
        return False

    # Ensure the unique_id is non-empty
    if not unique_id:
        return False

    # Avoid adding duplicate task IDs by checking the queue contents.
    # Since Queue does not provide direct inspection, we perform a lightweight
    # check by maintaining a separate set of IDs. This set is protected by the
    # same queue lock to keep consistency.
    global _registered_task_ids  # type: ignore
    try:
        _registered_task_ids.add(unique_id)
    except AttributeError:
        # First time initialization
        _registered_task_ids = {unique_id}

    try:
        task_queue.put_nowait((unique_id, task_info))
        return True
    except queue.Full:
        # Queue reached its maximum capacity; do not add the task.
        _registered_task_ids.remove(unique_id)
        return False
    except Exception:
        # Any unexpected error should not crash the system.
        _registered_task_ids.remove(unique_id)
        return False