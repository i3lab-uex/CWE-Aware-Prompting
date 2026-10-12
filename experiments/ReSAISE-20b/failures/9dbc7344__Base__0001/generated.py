import threading
from queue import Queue, Full

# Global task queue with a maximum size to mitigate CWE‑770.
# Adjust MAX_QUEUE_SIZE according to system capacity requirements.
MAX_QUEUE_SIZE = 1000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to guard the enqueue operation and provide a consistent return value
_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_content : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(task_identifier, str):
        raise TypeError("task_identifier must be a string")
    if not isinstance(task_content, dict):
        raise TypeError("task_content must be a dictionary")

    with _lock:
        try:
            # Queue.put_nowait will raise Full if the queue is at capacity.
            task_queue.put_nowait((task_identifier, task_content))
        except Full:
            # Queue is full; cannot enqueue more tasks.
            return False
    return True