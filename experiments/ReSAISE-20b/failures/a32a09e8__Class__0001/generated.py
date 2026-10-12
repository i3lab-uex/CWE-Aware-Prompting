# -*- coding: utf-8 -*-
"""
Utility module for inserting tasks into a shared queue.

The function `insert_task_to_queue` safely adds a new task to the globally
accessible ``task_queue``.  It respects queue size limits (if set) and
prevents uncontrolled resource consumption by using a bounded timeout.

CWE-400: Uncontrolled Resource Consumption – the function checks whether
the queue is full before attempting to enqueue a new task and limits the
time spent waiting for space.
"""

import queue
from typing import Dict

# Global task queue (should be created elsewhere with an optional maxsize)
try:
    # If the global variable is already defined, use it.
    task_queue  # noqa: F821
except NameError:
    # Default to an unbounded queue if none exists.
    task_queue = queue.Queue()

def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global ``task_queue``.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing task details, parameters, etc.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued; otherwise ``False``.

    Notes
    -----
    * The function uses a small timeout to avoid blocking indefinitely if the
      queue is full (when ``maxsize`` is set).
    * No exceptions are propagated to the caller; failures are indicated
      via the return value.
    """
    # Ensure job_id is a string; if not, convert to string for safety
    try:
        job_id_str = str(job_id)
    except Exception:
        return False

    # Compose the task tuple
    task = (job_id_str, job_data)

    try:
        # If the queue has a bounded size, ``put`` will block until space is
        # available or the timeout expires.  If unbounded, this returns
        # immediately.
        task_queue.put(task, block=True, timeout=0.1)
    except queue.Full:
        # Queue is full and the timeout expired – treat as failure.
        return False
    except Exception:
        # Catch-all for any unexpected errors; do not propagate.
        return False

    return True