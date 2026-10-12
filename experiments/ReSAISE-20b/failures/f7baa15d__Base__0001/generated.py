import queue
from typing import Dict

# Global task queue with a hard limit to avoid resource exhaustion (CWE‑770 mitigation).
# The maxsize can be tuned according to the deployment environment.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[Dict[str, object]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Safely add a task to the global queue.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic validation to avoid malicious payloads
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Attach the task_id to the data payload
    queued_task = {"task_id": task_id, "data": task_data}

    try:
        # Non-blocking put; returns False if the queue is full
        task_queue.put_nowait(queued_task)
    except queue.Full:
        # Queue has reached its limit; reject the task
        return False

    return True