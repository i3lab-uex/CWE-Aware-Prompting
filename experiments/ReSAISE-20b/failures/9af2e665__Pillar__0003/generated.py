# -*- coding: utf-8 -*-
"""
Utility module for managing a global task queue in a parallel processing system.
"""

import queue
from typing import Dict

# Global, thread‑safe queue used by the system.
task_queue: queue.Queue = queue.Queue()


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information about the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic type validation – avoid accidental injection of malicious objects
    if not isinstance(task_uid, str) or not isinstance(task_info, dict):
        return False

    # The queue is already thread‑safe; use put_nowait to avoid blocking.
    try:
        task_queue.put_nowait((task_uid, task_info))
    except queue.Full:
        # Queue capacity exceeded; log or handle as needed.
        return False
    except Exception:
        # Catch any unforeseen errors (e.g., serialization issues)
        return False

    return True