import threading
from queue import Queue

# Global, thread‑safe task queue
task_queue: Queue = Queue()

def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global `task_queue`.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Prepare the task payload
    task_payload = {
        "id": unique_task_id,
        "info": task_info,
    }

    try:
        # Enqueue the task. `put_nowait` will raise queue.Full if the
        # internal buffer is full, which we treat as a failure.
        task_queue.put_nowait(task_payload)
    except Exception:
        # Any exception (including queue.Full) results in a failure.
        return False

    return True