from queue import Queue
import threading

# Global task queue used by the system.
task_queue: Queue = Queue()

def insert_task_to_queue(job_id: str, job_data: dict) -> bool:
    """
    Insert a new task into the global task queue.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing task details, parameters, etc.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to avoid accidental injection of malicious data
    if not isinstance(job_id, str) or not job_id.strip():
        return False

    if not isinstance(job_data, dict):
        return False

    # Ensure the task payload is serializable (e.g., no non-JSON types)
    try:
        # Using a shallow copy to avoid accidental modifications after enqueue
        payload = {"job_id": job_id, "job_data": dict(job_data)}
    except Exception:
        return False

    try:
        # Queue.put_nowait() raises queue.Full if the queue is bounded and full
        task_queue.put_nowait(payload)
    except Exception:
        return False

    return True