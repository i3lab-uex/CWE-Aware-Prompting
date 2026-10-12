import queue
from threading import Lock

# Global task queue with a reasonable maximum size to mitigate CWE‑770.
# The limit can be tuned based on system resources and expected workload.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect the size check and put operation atomically
_queue_lock = Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global queue in a thread‑safe manner.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        A dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic validation
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Use a lock to ensure atomicity of the size check and put operation
    with _queue_lock:
        if task_queue.full():
            # Queue has reached its maximum capacity; reject the new task
            return False
        try:
            # Store as a tuple to keep both id and data together
            task_queue.put_nowait((task_id, task_data))
        except queue.Full:
            # This should not happen because we checked above,
            # but handle it defensively
            return False

    return True