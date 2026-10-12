import queue
import threading

# Global task queue used by the application
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue()

# A set that keeps track of all task identifiers currently in the queue
_task_registry: set[str] = set()

# A lock to guard access to _task_registry and the queue
_task_lock = threading.RLock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique string that identifies the task.
    parameters : dict
        The arguments and configuration for the task.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False if a task with the same reference already exists.

    Notes
    -----
    The function is thread‑safe and protects the global registry from race
    conditions. It does not raise exceptions; if a duplicate is detected,
    the task is simply rejected.
    """
    # Basic input validation
    if not isinstance(task_reference, str):
        raise TypeError("task_reference must be a string")
    if not isinstance(parameters, dict):
        raise TypeError("parameters must be a dictionary")

    with _task_lock:
        if task_reference in _task_registry:
            # Duplicate task – do not enqueue
            return False

        # Register the task and enqueue it
        _task_registry.add(task_reference)
        try:
            task_queue.put((task_reference, parameters))
        except Exception:  # pragma: no cover
            # Rollback registration if enqueue fails for any reason
            _task_registry.remove(task_reference)
            return False

    return True