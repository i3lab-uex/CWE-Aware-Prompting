# -*- coding: utf-8 -*-
"""
Task queueing module for a multi‑threaded system.

This module exposes a single public function, `queue_new_task`, which
appends a task to the global :data:`task_queue`.  The queue is thread‑safe
and can be safely accessed from multiple producers and consumers.
"""

import queue
from typing import Dict, Any

# Global thread‑safe queue used by the application.
task_queue: queue.Queue[tuple[str, Dict[str, Any]]] = queue.Queue()


def queue_new_task(unique_task_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Append a new task to the global :data:`task_queue`.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.  It is used as a key when the
        consumer processes the task, but this function does not enforce
        uniqueness.
    task_info : dict
        A dictionary containing the parameters and details for the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued; otherwise
        ``False``.  The function never raises an exception – any
        failure is silently converted to a ``False`` return value.

    Notes
    -----
    * The function is deliberately tolerant of errors to keep the producer
      side simple.  In production code you might want to log failures or
      raise exceptions instead.
    * ``queue.Queue`` is unbounded by default; if you need a bounded queue
      replace the global instance with ``queue.Queue(maxsize=N)``.
    """
    try:
        # Store as a tuple so consumers can easily unpack the ID and info.
        task_queue.put((unique_task_id, task_info))
        return True
    except Exception:
        # In a real system you might log the exception here.
        return False