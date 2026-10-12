import threading
from queue import Queue, Full

# Global task queue used by the system.
# Using a thread-safe FIFO queue to store tasks.
task_queue = Queue()

def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global task queue.

    Args:
        identifier (str): Unique string identifying the task.
        details (dict): Dictionary of parameters for the task.

    Returns:
        bool: True if the task was successfully queued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    # Construct the task payload
    task_payload = {"id": identifier, "details": details}

    try:
        # Attempt to enqueue the task.
        # `put_nowait` raises Full if the queue has a maxsize and is full.
        task_queue.put_nowait(task_payload)
    except Full:
        # Queue reached its maximum capacity (unlikely with unlimited queue).
        return False
    except Exception:
        # Catch-all for unexpected errors; log if needed.
        return False

    return True