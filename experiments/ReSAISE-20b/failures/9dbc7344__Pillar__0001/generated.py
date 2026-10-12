import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue: Queue = Queue(maxsize=1000)  # adjust maxsize as needed

def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_content : dict
        Dictionary containing task parameters and data.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation to avoid corrupt data
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_content, dict):
        return False

    # Construct the task payload
    task_payload = {
        "id": task_identifier,
        "content": task_content,
        "timestamp": threading.get_native_id(),  # example of additional metadata
    }

    try:
        # Non‑blocking put to avoid hanging the caller
        task_queue.put_nowait(task_payload)
    except Full:
        # Queue is full; could log or handle as needed
        return False

    return True