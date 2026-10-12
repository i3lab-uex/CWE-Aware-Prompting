import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue: Queue = Queue()

def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        Dictionary containing the specifics and parameters of the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid accidental injection of malicious objects
    if not isinstance(task_identifier, str) or not isinstance(task_content, dict):
        return False

    # Create a lightweight task representation
    task = {"id": task_identifier, "content": task_content}

    try:
        # Use put_nowait for non‑blocking enqueue
        task_queue.put_nowait(task)
    except Full:
        # Queue is full (unlikely with default infinite size)
        return False
    except Exception:
        # Catch-all for unforeseen errors; do not raise
        return False

    return True