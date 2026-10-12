import queue
from typing import Dict

# Global task queue – thread‑safe FIFO
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()


def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Parameters and specifics of the task.

    Returns
    -------
    bool
        True if enqueued successfully, False otherwise.
    """
    try:
        # Ensure the task is a tuple (id, info) for consistency
        task_queue.put_nowait((unique_task_id, task_info))
    except queue.Full:
        # Queue is full – cannot enqueue
        return False
    except Exception:
        # Any other exception (unlikely with Queue) – log if needed
        return False

    return True