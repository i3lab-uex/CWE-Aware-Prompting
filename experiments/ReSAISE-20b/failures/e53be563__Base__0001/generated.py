import queue
import threading

# Global task queue with a configurable maximum size to avoid unbounded resource usage.
MAX_QUEUE_SIZE = 1000          # Adjust this limit based on system capacity
_task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# A set to track registered UIDs and prevent duplicate tasks.
_registered_uids: set[str] = set()
_uid_lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Add a new task to the global queue if it does not exceed capacity
    and its UID has not been registered yet.

    Args:
        uid: Unique identifier for the task.
        data: Dictionary containing task parameters.

    Returns:
        bool: True if the task was successfully queued, False otherwise.
    """
    # Ensure UID uniqueness
    with _uid_lock:
        if uid in _registered_uids:
            return False  # Duplicate UID; reject the task
        _registered_uids.add(uid)

    try:
        # Attempt to enqueue without blocking. If the queue is full, it will raise Full.
        _task_queue.put_nowait((uid, data))
    except queue.Full:
        # Queue is full; rollback UID registration
        with _uid_lock:
            _registered_uids.discard(uid)
        return False

    return True