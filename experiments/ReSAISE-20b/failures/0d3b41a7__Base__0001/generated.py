import queue
import threading

# Global task queue with a reasonable maximum size to avoid resource exhaustion.
# Adjust MAX_QUEUE_SIZE according to system capacity.
MAX_QUEUE_SIZE = 10000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# Keeps track of task IDs that are already queued to prevent duplicates.
queued_task_ids: set[str] = set()
# Lock protects both the queue and the ID set.
_queue_lock = threading.Lock()


def queue_new_task(unique_task_id: str, task_info: dict) -> bool:
    """
    Append a new task to the global task queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing the task's parameters and specifics.

    Returns
    -------
    bool
        True if the task was successfully enqueued; False otherwise.
    """
    # Basic type validation (no exception raised, just a safe guard)
    if not isinstance(unique_task_id, str) or not isinstance(task_info, dict):
        return False

    with _queue_lock:
        # Avoid duplicate tasks
        if unique_task_id in queued_task_ids:
            return False

        # Check for queue capacity
        if task_queue.full():
            return False

        try:
            # Enqueue the task tuple
            task_queue.put_nowait((unique_task_id, task_info))
        except queue.Full:
            return False

        # Record the ID to prevent duplicates
        queued_task_ids.add(unique_task_id)

    return True