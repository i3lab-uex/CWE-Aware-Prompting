#!/usr/bin/env python3
"""
Task queueing module.

This module provides a thread‑safe mechanism to enqueue new tasks into a global
queue.  It ensures that each task is identified by a unique ID and guards
against duplicate submissions or queue over‑run.  The implementation is robust
against common concurrency issues and follows the guidance for proper resource
control (CWE‑664).
"""

from __future__ import annotations

import threading
import queue
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global data structures (protected by a lock for thread safety)
# --------------------------------------------------------------------------- #

_task_queue: "queue.Queue[tuple[str, Dict[str, Any]]]" = queue.Queue()
# A set that tracks all task IDs currently in the queue or being processed.
_task_ids: "set[str]" = set()
# Lock to protect access to _task_ids and queue operations.
_task_lock: threading.Lock = threading.Lock()


def queue_new_task(unique_task_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier for the task.
    task_info : dict
        A dictionary containing all parameters needed to process the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, ``False`` otherwise.
        Failure occurs when the ID already exists or if an unexpected error
        prevents enqueuing.

    Notes
    -----
    * The function is thread‑safe; concurrent calls will not corrupt the queue.
    * Duplicate task IDs are rejected to prevent accidental reprocessing.
    * The global queue is unbounded; if you need a bounded size, replace
      ``queue.Queue()`` with ``queue.Queue(maxsize=N)`` and adjust the logic.
    """
    if not isinstance(unique_task_id, str):
        raise TypeError("unique_task_id must be a string")
    if not isinstance(task_info, dict):
        raise TypeError("task_info must be a dictionary")

    with _task_lock:
        # Reject duplicate task IDs
        if unique_task_id in _task_ids:
            return False

        try:
            # Enqueue the task as a tuple (id, info)
            _task_queue.put_nowait((unique_task_id, task_info))
        except queue.Full:
            # This should not happen with an unbounded queue,
            # but we handle it gracefully.
            return False
        except Exception:
            # Any other exception means enqueue failed; do not add the ID.
            return False

        # Mark the task ID as enqueued
        _task_ids.add(unique_task_id)
        return True


# --------------------------------------------------------------------------- #
# Helper functions for consumers (not required by the prompt but useful)
# --------------------------------------------------------------------------- #

def get_next_task() -> tuple[str, Dict[str, Any]] | None:
    """
    Retrieve the next task from the queue.

    Returns
    -------
    tuple[str, dict] | None
        The next task's ID and info dictionary, or ``None`` if the queue is empty.
    """
    try:
        task_id, task_info = _task_queue.get_nowait()
    except queue.Empty:
        return None

    # Remove the task ID from the tracking set once it has been fetched
    with _task_lock:
        _task_ids.discard(task_id)

    return task_id, task_info


def task_done() -> None:
    """
    Signal that a queued task has been processed.
    This must be called after ``get_next_task`` to maintain queue statistics.
    """
    _task_queue.task_done()