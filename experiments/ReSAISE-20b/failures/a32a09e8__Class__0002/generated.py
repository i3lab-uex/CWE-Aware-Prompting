import queue
from typing import Dict

# Global task queue (should be instantiated elsewhere in the application)
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # example max size


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing task details.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation: ensure job_id is a string and job_data is a dict
    if not isinstance(job_id, str) or not isinstance(job_data, dict):
        return False

    # Construct the task payload
    task = {"job_id": job_id, "job_data": job_data}

    try:
        # Use put_nowait to avoid blocking; if the queue is full, catch Full exception
        task_queue.put_nowait(task)
    except queue.Full:
        # Queue has reached its maximum capacity – reject the task
        return False

    return True