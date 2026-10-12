import queue
from typing import Dict

# Global task queue with a reasonable maximum size to mitigate CWE-770.
# Adjust MAX_QUEUE_SIZE as appropriate for the application context.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global task queue.

    Parameters
    ----------
    job_id : str
        A unique string identifier for the task.
    job_data : dict
        Dictionary containing task parameters and other metadata.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic type validation
    if not isinstance(job_id, str) or not isinstance(job_data, dict):
        return False

    try:
        # The put_nowait call will raise queue.Full if the queue is at capacity.
        task_queue.put_nowait((job_id, job_data))
    except queue.Full:
        # Queue is full; cannot accept new tasks at this time.
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking resources.
        return False

    return True