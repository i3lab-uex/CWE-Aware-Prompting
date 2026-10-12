import queue

# Global task queue (must be initialized elsewhere in the system)
task_queue: queue.Queue = None  # type: ignore

def insert_task_to_queue(job_id: str, job_data: dict) -> bool:
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
        True if the task was added successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(job_id, str) or not job_id:
        return False
    if not isinstance(job_data, dict):
        return False

    # Ensure the global queue is available
    if task_queue is None:
        return False

    # Prevent uncontrolled resource consumption: check queue capacity
    try:
        if task_queue.maxsize > 0 and task_queue.qsize() >= task_queue.maxsize:
            # Queue is full; refuse to add more tasks
            return False

        # Prepare the task payload
        task_payload = {"job_id": job_id, "job_data": job_data}

        # Attempt to put the task into the queue without blocking
        task_queue.put_nowait(task_payload)
        return True

    except (queue.Full, queue.Empty):
        # Queue is full or other queue-related issue
        return False
    except Exception:
        # Catch-all for unexpected errors; do not raise
        return False