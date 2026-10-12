# -*- coding: utf-8 -*-
"""
Utility to safely enqueue tasks into a global multiprocessing queue.
This module mitigates uncontrolled resource consumption by enforcing
a maximum queue size and validating input before insertion.
"""

from multiprocessing import Queue, current_process
import threading
import time
from typing import Dict

# Global task queue. In a real application this would be created once
# and shared across processes/threads.
task_queue: Queue = Queue(maxsize=1000)  # Example max size, adjust as needed

# Lock to serialize access when using threading (multiprocessing.Queue is process-safe)
_queue_lock = threading.Lock()


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Safely insert a task into the global task queue.

    Args:
        job_id (str): Unique identifier for the task.
        job_data (dict): Dictionary containing task details and parameters.

    Returns:
        bool: True if the task was successfully queued, False otherwise.
    """
    # Basic validation
    if not isinstance(job_id, str) or not job_id:
        return False
    if not isinstance(job_data, dict):
        return False

    # Prevent excessive memory usage by checking queue size
    try:
        with _queue_lock:
            if task_queue.full():
                # Optionally log or handle the overflow condition
                return False

            # Prepare the task payload; could include metadata if needed
            task_payload = {
                "job_id": job_id,
                "job_data": job_data,
                "timestamp": time.time(),
                "producer_process": current_process().name
            }

            task_queue.put(task_payload, block=False)
        return True

    except Exception:
        # Silently swallow exceptions to comply with "Raise: None"
        return False