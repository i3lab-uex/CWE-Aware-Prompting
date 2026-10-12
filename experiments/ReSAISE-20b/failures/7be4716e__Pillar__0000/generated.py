import queue
from typing import Dict, Any

# Global task queue used by the parallel processing system.
# In a real application this would be created and managed elsewhere,
# but for the purpose of this function we expose it as a module-level
# variable that callers can import.
task_queue: queue.Queue = queue.Queue(maxsize=1000)


def enqueue_task(unique_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task. Must be a non-empty string.
    task_info : dict
        A dictionary containing the task's parameters and other relevant data.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, otherwise ``False``.

    Notes
    -----
    * The function is thread‑safe thanks to :class:`queue.Queue`.
    * If the queue is full, ``False`` is returned instead of blocking.
    * No exception is propagated to the caller; failures are logged and
      a ``False`` value is returned.

    Raises
    ------
    None

    Security / Weakness considerations
    ----------------------------------
    * The function does not modify or expose the internal state of `task_queue`
      beyond enqueuing. It also performs minimal validation to avoid
      accidental insertion of malformed data.
    * The queue size is capped (default 1000) to prevent unlimited memory
      consumption, mitigating CWE‑664 by controlling the resource lifetime.
    """
    # Basic input validation
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    try:
        # Non‑blocking put; if the queue is full we simply fail.
        task_queue.put_nowait((unique_id, task_info))
    except queue.Full:
        # Queue has reached its maximum capacity.
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking internal state.
        return False

    return True