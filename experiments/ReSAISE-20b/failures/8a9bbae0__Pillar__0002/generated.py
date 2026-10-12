# task_queue_module.py

import queue
import threading
from typing import Dict, Tuple

# Global task queue – thread‑safe by design (queue.Queue)
task_queue: "queue.Queue[Tuple[str, Dict]]" = queue.Queue()

# Lock to guard against duplicate task identifiers if needed
_task_id_lock = threading.Lock()
_registered_ids: set[str] = set()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        Parameters and details required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    * The function is thread‑safe.
    * Duplicate task identifiers are ignored to prevent accidental reprocessing.
    * No exceptions propagate; failures result in a ``False`` return value.
    """
    if not isinstance(task_identifier, str) or not isinstance(task_details, dict):
        # Basic type validation – could also raise an exception if desired
        return False

    with _task_id_lock:
        # Avoid enqueuing a task with an already registered identifier
        if task_identifier in _registered_ids:
            return False
        _registered_ids.add(task_identifier)

    try:
        # Enqueue the task as a tuple (identifier, details)
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue is full – clean up the identifier set
        with _task_id_lock:
            _registered_ids.discard(task_identifier)
        return False
    except Exception:
        # Unexpected error – also clean up
        with _task_id_lock:
            _registered_ids.discard(task_identifier)
        return False

    return True