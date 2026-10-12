import queue
from typing import Dict

# Global task queue used by the parallel processing system.
task_queue: queue.Queue = queue.Queue(maxsize=0)  # unbounded by default

def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details, parameters, and other metadata.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.

    Notes
    -----
    - The function is thread‑safe because `queue.Queue` handles its own locking.
    - If the queue is full (in a bounded scenario), this function will block until space
      becomes available. For an unbounded queue this should never happen.
    - No exceptions are propagated; failures are indicated via the return value.
    """
    try:
        # The tuple stores both UID and info to preserve uniqueness and context
        task_queue.put((task_uid, task_info), block=True)
        return True
    except Exception:
        # In a production setting we might log the exception here.
        return False