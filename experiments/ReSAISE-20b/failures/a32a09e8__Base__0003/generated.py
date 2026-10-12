import queue
from typing import Dict

# Global task queue with a reasonable maximum size to avoid unbounded growth.
# The maxsize can be tuned according to system resources; here we set it to 10_000.
task_queue: queue.Queue = queue.Queue(maxsize=10000)


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(job_id, str) or not job_id:
        return False

    if not isinstance(job_data, dict):
        return False

    # Prepare the task payload
    task_payload = {"job_id": job_id, "job_data": job_data}

    try:
        # Use put_nowait to avoid blocking; if the queue is full, return False.
        task_queue.put_nowait(task_payload)
    except queue.Full:
        # Queue has reached its maxsize; do not block or raise.
        return False

    return True