# -*- coding: utf-8 -*-
"""
Module providing a thread‑safe task queue interface.

The global `task_queue` holds pending tasks.  The function
`add_task_to_queue()` adds a new task to the queue while guarding
against race conditions and ensuring that resources are properly
managed.
"""

from __future__ import annotations

import queue
import threading
from typing import Dict, Tuple

# Global task queue (FIFO).  The `queue.Queue` class is already
# thread‑safe and handles all necessary locking internally.
task_queue: queue.Queue[Tuple[str, Dict]] = queue.Queue()

# Optional lock for additional atomic checks (e.g., deduplication).
# In this example we only use the queue's own locking, but a lock
# is kept to demonstrate how one might extend the logic.
_queue_lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    task_id : str
        Unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        ``True`` if the task was successfully added to the queue,
        otherwise ``False``.

    Notes
    -----
    * The function is safe to call from multiple threads.
    * No explicit resource cleanup is required because the queue
      manages its own internal state.  The function simply enqueues
      a tuple ``(task_id, task_data)``.
    """
    # Validate input types to avoid accidental misuse.
    if not isinstance(task_id, str):
        return False
    if not isinstance(task_data, dict):
        return False

    try:
        # Acquire a lock only if additional atomic checks are needed.
        with _queue_lock:
            # Enqueue the task.  `put_nowait` raises ``Full`` if a
            # maximum size is set and the queue is full.
            task_queue.put_nowait((task_id, task_data))
        return True
    except queue.Full:
        # Queue is full; could log or handle as needed.
        return False
    except Exception:
        # Catch-all for unforeseen errors; returning False signals failure.
        return False