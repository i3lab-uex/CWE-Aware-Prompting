# SPDX-License-Identifier: MIT

"""
Task queue management module.

This module provides a thread‑safe way to enqueue tasks into a global
queue while protecting against uncontrolled resource consumption
(CWE-400).  The queue is bounded and the enqueue operation will fail
gracefully if the maximum size is reached.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import threading
from queue import Queue, Full
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Maximum number of tasks that can be queued at any one time.
MAX_QUEUE_SIZE = 10_000

# --------------------------------------------------------------------------- #
# Global queue
# --------------------------------------------------------------------------- #

# The global task queue.  It is bounded to prevent unlimited memory usage.
task_queue: Queue[tuple[str, Dict[str, Any]]] = Queue(maxsize=MAX_QUEUE_SIZE)

# A lock to protect the size check and enqueue operation from race conditions.
_queue_lock = threading.Lock()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def enqueue_task(identifier: str, details: Dict[str, Any]) -> bool:
    """
    Enqueue a new task into the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        A dictionary containing parameters and metadata for the task.

    Returns
    -------
    bool
        ``True`` if the task was added successfully, ``False`` otherwise.

    Notes
    -----
    * The function is thread‑safe.
    * The queue has a fixed maximum size.  If the queue is full, the
      function returns ``False`` instead of blocking or raising an exception.
    * No exceptions are raised; the caller can inspect the return value.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str):
        raise TypeError("identifier must be a string")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    with _queue_lock:
        if task_queue.full():
            # Queue is at capacity – do not block or raise
            return False

        try:
            task_queue.put_nowait((identifier, details))
            return True
        except Full:
            # This should not happen because we checked `full()` earlier,
            # but handle it defensively.
            return False