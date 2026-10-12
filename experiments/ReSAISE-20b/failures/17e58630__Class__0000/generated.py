import queue
import threading

# Global queue and helper structures (create if not already defined)
try:
    task_queue
except NameError:  # pragma: no cover
    # Default maxsize can be tuned to avoid uncontrolled resource consumption.
    task_queue = queue.Queue(maxsize=1000)

# A set to keep track of identifiers that are currently queued.
try:
    _queued_ids
except NameError:  # pragma: no cover
    _queued_ids = set()

# Lock to protect access to the identifier set and queue operations.
_queue_lock = threading.Lock()


def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Parameters and data for the task.

    Returns
    -------
    bool
        ``True`` if the task was enqueued, ``False`` otherwise (e.g. duplicate
        identifier or queue full).

    Notes
    -----
    * The function is thread‑safe.
    * It prevents uncontrolled growth by respecting the queue's ``maxsize``.
    * Duplicate identifiers are rejected to avoid duplicate work.
    """
    if not isinstance(identifier, str) or not isinstance(details, dict):
        # Basic type validation to avoid malformed entries.
        return False

    with _queue_lock:
        if identifier in _queued_ids:
            # Duplicate task; do not enqueue again.
            return False

        try:
            # Attempt to enqueue without blocking.
            task_queue.put_nowait((identifier, details))
        except queue.Full:
            # Queue reached its capacity; cannot accept new tasks.
            return False

        # Mark identifier as queued.
        _queued_ids.add(identifier)
        return True