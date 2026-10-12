import queue
from typing import Dict

# Global task queue used by the system.
# It should be created once during system initialization.
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # Example size limit


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Safely insert a new task into the global task queue.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False otherwise (e.g., invalid input, full queue).
    """
    # Basic validation to avoid malformed inputs.
    if not isinstance(job_id, str) or not isinstance(job_data, dict):
        return False

    # Construct the task payload.
    task_payload = {"job_id": job_id, "job_data": job_data}

    try:
        # Use put_nowait to avoid blocking the caller.
        task_queue.put_nowait(task_payload)
    except queue.Full:
        # Queue is full; cannot add the task.
        return False
    except Exception:
        # Any other unexpected exception is treated as a failure.
        return False

    return True