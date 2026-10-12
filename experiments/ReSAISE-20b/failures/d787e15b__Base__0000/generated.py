#!/usr/bin/env python3
"""
Utility module for registering new tasks in a shared queue.

This implementation protects against unchecked growth of the task queue
(CWE‑770) by enforcing a maximum size.  It also tracks registered task
identifiers to guarantee uniqueness.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import threading
from queue import Queue, Full, Empty
from typing import Dict, Optional


# --------------------------------------------------------------------------- #
# Configuration: Maximum number of tasks that can be queued at once.
# --------------------------------------------------------------------------- #
MAX_TASK_QUEUE_SIZE = 1000  # Adjust as needed for your environment


# --------------------------------------------------------------------------- #
# Global data structures
# --------------------------------------------------------------------------- #
_task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=MAX_TASK_QUEUE_SIZE)
_registered_task_ids: set[str] = set()
_registry_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task for execution.

    Parameters
    ----------
    task_reference : str
        Unique identifier of the task.
    parameters : dict
        Parameters required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.

    Notes
    -----
    * The function is thread‑safe and respects the configured maximum queue size.
    * Duplicate task identifiers are rejected to prevent accidental overwrites.
    """
    if not isinstance(task_reference, str):
        raise TypeError("task_reference must be a string")
    if not isinstance(parameters, dict):
        raise TypeError("parameters must be a dictionary")

    # Ensure uniqueness of the task identifier
    with _registry_lock:
        if task_reference in _registered_task_ids:
            # Duplicate identifier; do not enqueue
            return False

        try:
            _task_queue.put_nowait((task_reference, parameters))
        except Full:
            # Queue has reached its maximum capacity
            return False

        # Registration successful; record the identifier
        _registered_task_ids.add(task_reference)
        return True


# --------------------------------------------------------------------------- #
# Optional helper functions (for testing / introspection)
# --------------------------------------------------------------------------- #

def _pop_task() -> Optional[tuple[str, Dict]]:
    """
    Pop a task from the queue for processing.  This function is internal and
    not part of the public API.
    """
    try:
        task = _task_queue.get_nowait()
    except Empty:
        return None
    else:
        with _registry_lock:
            # Remove the identifier from the registry when processed
            _registered_task_ids.discard(task[0])
        return task


def queue_size() -> int:
    """Return the current number of queued tasks."""
    return _task_queue.qsize()


def registered_task_count() -> int:
    """Return the number of unique task identifiers currently registered."""
    with _registry_lock:
        return len(_registered_task_ids)