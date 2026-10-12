import queue
from typing import Dict

# Global task queue shared by all workers.
task_queue: queue.Queue = queue.Queue()

# Optional upper bound on the number of tasks that can be queued.
MAX_QUEUE_SIZE = 10_000  # Adjust as needed for your system.

def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Safely insert a new task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing all relevant data for the task.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Validate inputs quickly
    if not isinstance(job_id, str) or not job_id:
        return False
    if not isinstance(job_data, dict):
        return False

    # Prevent unbounded growth (CWE-770 mitigation)
    try:
        if task_queue.qsize() >= MAX_QUEUE_SIZE:
            # Queue is full; refuse to add more tasks
            return False

        # Insert the task atomically
        task_queue.put_nowait((job_id, job_data))
        return True

    except queue.Full:
        # Rare race condition where the queue became full after the size check
        return False

    except Exception:
        # Catch-all for unforeseen errors; do not raise to caller
        return False