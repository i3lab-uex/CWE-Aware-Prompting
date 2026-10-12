#!/usr/bin/env python3
"""
Utility for safely adding tasks to a shared queue in a concurrent environment.
"""

import queue
from typing import Dict

# Define the global task queue with a reasonable maximum size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE as appropriate for the deployment environment.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def push_task(uid: str, data: Dict) -> bool:
    """
    Attempt to add a new task identified by `uid` and associated with `data`
    to the global `task_queue`.

    Parameters
    ----------
    uid : str
        A unique identifier for the task.
    data : dict
        Task payload containing parameters and details.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate inputs
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    try:
        # The put_nowait method raises queue.Full if the queue is at its maxsize.
        task_queue.put_nowait((uid, data))
        return True
    except queue.Full:
        # Queue is full; reject the task to avoid uncontrolled resource consumption.
        return False