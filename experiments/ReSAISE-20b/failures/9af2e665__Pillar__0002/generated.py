# -*- coding: utf-8 -*-

"""
Utilities for task queue management in a parallel processing system.
"""

from __future__ import annotations

import logging
from queue import Queue, Full, Empty
from typing import Dict, Any

# Configure module-level logger
_logger = logging.getLogger(__name__)

# Global task queue instance.  It is expected to be created elsewhere
# and imported into this module.  For demonstration purposes we create it here.
task_queue: Queue[tuple[str, Dict[str, Any]]] = Queue(maxsize=1000)


def push_task_to_queue(task_uid: str, task_info: Dict[str, Any]) -> bool:
    """
    Add a new task to the global ``task_queue``.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information about the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, ``False`` otherwise.

    Notes
    -----
    * The function uses :py:meth:`queue.Queue.put_nowait` to avoid blocking
      indefinitely.  If the queue is full, ``Full`` is caught and a warning
      is logged.
    * The function does **not** raise any exception; it logs errors and
      returns ``False`` to signal failure.
    * This implementation guards against improper resource control by
      ensuring that the queue object is accessed in a thread‑safe manner
      (the :class:`queue.Queue` class already provides the necessary locking).
    """
    try:
        # Ensure that task_uid is a string; if not, convert it.
        uid = str(task_uid)

        # Basic validation of task_info
        if not isinstance(task_info, dict):
            _logger.error("task_info must be a dictionary; got %s", type(task_info))
            return False

        # Attempt to enqueue the task without blocking
        task_queue.put_nowait((uid, task_info))
    except Full:
        _logger.warning("Task queue is full; cannot enqueue task %s", uid)
        return False
    except Exception as exc:  # pragma: no cover - defensive programming
        _logger.exception("Unexpected error while pushing task %s to queue: %s", uid, exc)
        return False

    return True