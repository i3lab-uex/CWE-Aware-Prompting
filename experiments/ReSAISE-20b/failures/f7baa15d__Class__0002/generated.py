import threading
from queue import Queue, Full

# Define a global task queue with a maximum size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to system limits and expected workload.
MAX_QUEUE_SIZE = 10_000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to ensure thread‑safe operations on the queue if additional checks are needed.
_queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    task_id : str
        Unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False if the queue is full.
    """
    # Basic validation to avoid adding malformed entries
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    try:
        # Attempt to put the task into the queue without blocking.
        # If the queue is full, a Full exception will be raised and we return False.
        task_queue.put_nowait((task_id, task_data))
    except Full:
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking resources or crashing.
        return False

    return True