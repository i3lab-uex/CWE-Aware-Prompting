# -*- coding: utf-8 -*-
"""
Module providing a thread‑safe helper for enqueuing tasks.
"""

from __future__ import annotations

import threading
from queue import Queue, Full
from typing import Dict

# Global task queue used by the application.
task_queue: Queue[Dict[str, any]] = Queue()
# Lock to guard operations that need to be atomic with respect to
# task identification and queue state.
_task_lock = threading.RLock()


def push_task(uid: str, data: Dict) -> bool:
    """
    Safely add a new task to the global ``task_queue``.

    Parameters
    ----------
    uid : str
        A unique identifier for the task.  The function will not add a
        duplicate entry if an existing task with the same ``uid`` is
        already in the queue.
    data : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, ``False``
        otherwise (e.g. queue full or duplicate uid).

    Notes
    -----
    * The function is thread‑safe: a reentrant lock protects the check
      for duplicate ``uid`` and the actual queue insertion.
    * The queue is bounded by default (see :class:`queue.Queue`); if
      it becomes full the function will return ``False`` instead of
      raising an exception.
    """
    if not isinstance(uid, str):
        raise TypeError("uid must be a string")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    with _task_lock:
        # Check for duplicates in the queue
        for task in list(task_queue.queue):
            if task.get("uid") == uid:
                # Duplicate found; do not enqueue again
                return False

        try:
            task_queue.put_nowait({"uid": uid, "data": data})
        except Full:
            # Queue is full; indicate failure
            return False

    return True