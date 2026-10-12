# -*- coding: utf-8 -*-
"""
Thread‑safe task queue implementation.

This module defines a global `task_queue` that can be used by multiple
threads to enqueue tasks for later processing.  The queue is bounded
to avoid uncontrolled resource consumption (CWE‑400).  Tasks are stored
as tuples `(task_id, task_data)`.

Functions:
    add_task_to_queue(task_id: str, task_data: dict) -> bool
"""

from __future__ import annotations

import threading
from queue import Queue, Full
from typing import Dict

# --------------------------------------------------------------------------- #
# Configuration constants
# --------------------------------------------------------------------------- #

# Maximum number of tasks that can be queued at once.
# Adjust this value based on available memory and expected load.
MAX_QUEUE_SIZE: int = 10_000

# --------------------------------------------------------------------------- #
# Global task queue
# --------------------------------------------------------------------------- #

# The queue is thread‑safe by design.
task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Enqueue a new task for processing.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.  It is not checked for uniqueness
        by this function; callers must ensure that each ID is distinct.
    task_data : dict
        A dictionary containing task details and parameters.

    Returns
    -------
    bool
        ``True`` if the task was successfully added to the queue,
        ``False`` if the queue is full and the task could not be enqueued.

    Notes
    -----
    * The function is thread‑safe; it can be called from multiple threads.
    * The queue has a fixed maximum size (`MAX_QUEUE_SIZE`).  If the
      queue is full, ``add_task_to_queue`` returns ``False`` instead of
      blocking or raising an exception.  This prevents uncontrolled
      resource consumption (CWE‑400).
    """
    if not isinstance(task_id, str):
        raise TypeError("task_id must be a string")
    if not isinstance(task_data, dict):
        raise TypeError("task_data must be a dictionary")

    try:
        # ``put_nowait`` raises `Full` if the queue is at capacity.
        task_queue.put_nowait((task_id, task_data))
    except Full:
        # Queue is full; cannot accept more tasks.
        return False

    return True


# --------------------------------------------------------------------------- #
# Example usage (for testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import random
    import time

    def producer(thread_id: int):
        for i in range(5):
            task_id = f"t{thread_id}-{i}"
            data = {"value": random.randint(1, 100)}
            success = add_task_to_queue(task_id, data)
            print(f"[Producer {thread_id}] Task {task_id} queued: {success}")
            time.sleep(random.uniform(0.1, 0.5))

    # Start a few producer threads
    threads = [threading.Thread(target=producer, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Drain the queue
    while not task_queue.empty():
        tid, td = task_queue.get()
        print(f"[Consumer] Processing {tid}: {td}")