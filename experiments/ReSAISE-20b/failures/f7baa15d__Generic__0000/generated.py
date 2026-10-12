import threading
from queue import Queue

# Global task queue (unbounded by default)
task_queue = Queue()

# Lock to guard any additional consistency checks if needed
queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Adds a new task to the global task queue.

    Parameters
    ----------
    task_id : str
        Unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic validation: ensure inputs are of correct type
    if not isinstance(task_id, str) or not isinstance(task_data, dict):
        return False

    # Build the task payload
    task_payload = {"task_id": task_id, "data": task_data}

    try:
        # Use the queue's put_nowait to avoid blocking if the queue were bounded
        task_queue.put_nowait(task_payload)
        return True
    except Exception:
        # Any exception (e.g., queue full) results in a False return
        return False