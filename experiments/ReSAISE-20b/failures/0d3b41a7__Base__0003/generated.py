import threading
from queue import Queue, Full

# Global task queue with a reasonable maximum size to mitigate CWE-770
MAX_QUEUE_SIZE = 10_000   # adjust as appropriate for your environment
task_queue_lock = threading.Lock()
try:
    task_queue  # use existing global if present
except NameError:   # pragma: no cover
    task_queue = Queue(maxsize=MAX_QUEUE_SIZE)

def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and details.

    Returns
    -------
    bool
        True if the task was enqueued successfully; False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Construct the task payload
    task_payload = {"id": unique_task_id, "info": task_info}

    try:
        # Acquire lock to ensure atomicity with size check
        with task_queue_lock:
            if task_queue.full():
                # Queue is at capacity; reject new tasks
                return False
            # Use put_nowait to avoid blocking if the queue is full (extra safety)
            task_queue.put_nowait(task_payload)
    except Full:
        # In case of a race condition where the queue became full after the check
        return False

    return True