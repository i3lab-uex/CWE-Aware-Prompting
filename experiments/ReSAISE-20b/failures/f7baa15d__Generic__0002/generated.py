#!/usr/bin/env python3
"""
Thread‑safe task queue implementation.
"""

from __future__ import annotations

import threading
import queue
from typing import Dict, Any

# Global task queue (unbounded by default; change maxsize if desired)
task_queue: "queue.Queue[tuple[str, Dict[str, Any]]]" = queue.Queue()

# Set to keep track of task identifiers already in the queue
_task_ids: set[str] = set()

# Lock to protect access to _task_ids and task_queue
_task_lock: threading.Lock = threading.Lock()


def add_task_to_queue(task_id: str, task_data: Dict[str, Any]) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_id : str
        Unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    # Basic input validation
    if not isinstance(task_id, str) or not task_id:
        return False

    if not isinstance(task_data, dict):
        return False

    with _task_lock:
        # Reject duplicate task IDs
        if task_id in _task_ids:
            return False

        try:
            # Put the task into the queue (blocking if necessary)
            task_queue.put((task_id, task_data), block=False)
        except queue.Full:
            # In the unlikely event that a maxsize is set and full
            return False

        _task_ids.add(task_id)

    return True


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
if __name__ == "__main__":
    import time

    def worker():
        while True:
            try:
                t_id, t_data = task_queue.get(timeout=1)
                print(f"Processing {t_id}: {t_data}")
                time.sleep(0.5)  # Simulate work
                with _task_lock:
                    _task_ids.discard(t_id)
                task_queue.task_done()
            except queue.Empty:
                break

    # Add some tasks
    for i in range(5):
        add_task_to_queue(f"task-{i}", {"param": i})

    # Start worker threads
    workers = [threading.Thread(target=worker) for _ in range(2)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()

    print("All tasks processed.")