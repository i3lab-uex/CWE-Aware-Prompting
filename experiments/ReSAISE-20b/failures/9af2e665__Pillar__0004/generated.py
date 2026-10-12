# -*- coding: utf-8 -*-
"""
Utility for adding tasks to a global task queue in a parallel processing system.

The module assumes that a global `task_queue` object exists and is an instance of
either :class:`queue.Queue`, :class:`multiprocessing.Queue` or any object that
provides a ``put`` method with an optional ``block`` and ``timeout`` keyword.
"""

from __future__ import annotations

import sys
import traceback
from typing import Dict, Any

# Import the queue class that matches your environment.
# For example, if you are using multiprocessing:
try:
    from multiprocessing import Queue as _Queue
except Exception:  # pragma: no cover
    # Fallback to a standard queue if multiprocessing is unavailable.
    from queue import Queue as _Queue

# Global task queue.  In real code this would be initialized elsewhere.
# It must support the `put(item, block=True, timeout=None)` API.
task_queue: _Queue = _Queue()


def push_task_to_queue(task_uid: str, task_info: Dict[str, Any]) -> bool:
    """
    Safely push a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing all information needed to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.

    Notes
    -----
    * The function performs type validation on its arguments.
    * If the queue is full (when a timeout is specified) or if any exception
      occurs during `put`, the function returns ``False``.
    * No exceptions are propagated to callers, adhering to the requirement
      that this function never raises.
    """
    # Basic type validation – avoid accidental misuse and potential
    # serialization issues when the queue is backed by multiprocessing.
    if not isinstance(task_uid, str):
        return False
    if not isinstance(task_info, dict):
        return False

    # Construct the payload.  Include the UID for downstream consumers.
    payload = {"uid": task_uid, "info": task_info}

    try:
        # Use a short timeout to avoid blocking indefinitely; this also
        # mitigates potential deadlocks in long-running systems.
        task_queue.put(payload, block=True, timeout=1.0)
    except Exception:
        # Log the exception to stderr for debugging but do not raise.
        sys.stderr.write(
            f"[push_task_to_queue] Failed to enqueue task {task_uid}: "
            f"{traceback.format_exc()}\n"
        )
        return False

    return True