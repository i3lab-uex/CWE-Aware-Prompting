import queue
import threading

# Global task queue with a reasonable upper bound to mitigate CWE‑770.
# Adjust MAX_QUEUE_SIZE as needed for your deployment environment.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to protect insertion logic if additional checks are added later.
_insertion_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        Dictionary containing the task's parameters and details.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation to guard against malicious input
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    try:
        # Use a non-blocking put to avoid deadlocks; if the queue is full,
        # we simply return False.
        task_queue.put_nowait((task_identifier, task_content))
        return True
    except queue.Full:
        # Queue has reached its maximum size; caller can decide how to handle.
        return False