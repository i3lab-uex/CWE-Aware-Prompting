# -*- coding: utf-8 -*-
"""
Utility module for registering tasks into a shared queue in a concurrent environment.
"""

import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue: Queue = Queue(maxsize=0)  # unlimited size by default

# Lock to serialize access if needed (Queue already handles it, but kept for explicitness)
_queue_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global task queue.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Parameters and metadata associated with the task.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Construct the task payload
    task_payload = {
        "reference": task_reference,
        "parameters": parameters,
    }

    try:
        # Use non‑blocking put to avoid deadlock in full queues
        with _queue_lock:
            task_queue.put_nowait(task_payload)
    except Full:
        # Queue is full; cannot accept new task
        return False
    except Exception:  # pragma: no cover - defensive catch-all
        return False

    return True