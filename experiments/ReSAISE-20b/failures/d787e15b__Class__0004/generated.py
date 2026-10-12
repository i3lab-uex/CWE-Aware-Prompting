import threading
from queue import Queue, Full

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to your system's capacity requirements.
MAX_QUEUE_SIZE = 1000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to guard any additional shared state if needed in the future.
_queue_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global task queue.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Parameters associated with the task.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Attempt to put the task into the queue without blocking.
    try:
        with _queue_lock:
            task_queue.put_nowait((task_reference, parameters))
    except Full:
        # Queue is full; cannot accept more tasks at this time.
        return False

    return True