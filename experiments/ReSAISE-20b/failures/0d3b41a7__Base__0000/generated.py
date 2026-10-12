import queue
import threading

# Global task queue with a maximum size to avoid unlimited resource consumption (CWE‑770 mitigation).
MAX_QUEUE_SIZE = 10_000
_task_queue_lock = threading.Lock()
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.

    Notes
    -----
    * The function validates input types and uses a bounded queue to prevent unbounded memory
      growth (CWE‑770 mitigation).
    * Thread safety is ensured by using the queue's built-in locking mechanisms.
    """
    if not isinstance(unique_task_id, str):
        raise TypeError("unique_task_id must be a string")
    if not isinstance(task_info, dict):
        raise TypeError("task_info must be a dictionary")

    # Use put_nowait to avoid blocking; return False if queue is full.
    try:
        with _task_queue_lock:
            task_queue.put_nowait((unique_task_id, task_info))
        return True
    except queue.Full:
        # Queue is at capacity; cannot enqueue more tasks.
        return False