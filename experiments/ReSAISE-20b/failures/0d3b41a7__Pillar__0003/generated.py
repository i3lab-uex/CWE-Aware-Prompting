import queue
from typing import Dict

# Global task queue (thread‑safe)
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue()

def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing task specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    try:
        # The queue is thread‑safe; put_nowait will raise queue.Full if the
        # queue has a maxsize and is full. Since we do not set a maxsize,
        # this exception will not occur in normal operation.
        task_queue.put_nowait((unique_task_id, task_info))
    except Exception:
        # Any exception (e.g., serialization issues) results in a failure.
        return False
    else:
        return True