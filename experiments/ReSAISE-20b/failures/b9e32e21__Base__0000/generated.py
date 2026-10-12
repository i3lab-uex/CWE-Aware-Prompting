# activity_log.py

"""
Activity Log Module
~~~~~~~~~~~~~~~~~~~
Provides a simple function to record user actions in a global log list.
The module imposes a hard limit on the number of entries to mitigate
CWE-770 (unbounded resource allocation).
"""

# Global list that stores activity records.
activity_log = []

# Maximum number of entries allowed in the log.
MAX_LOG_ENTRIES = 1000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity_log.

    Parameters
    ----------
    uid : str
        Unique identifier of the user performing the action.
    act_description : str
        Textual description of the user's action.

    Returns
    -------
    bool
        True if the entry was added successfully.
        False if adding would exceed MAX_LOG_ENTRIES.

    Notes
    -----
    - The function is thread‑unsafe; if used in a multi‑threaded
      environment, external synchronization (e.g., a lock) is required.
    - No exceptions are raised; the caller must inspect the return value
      to determine success.
    """
    # Basic input validation: ensure both arguments are non-empty strings
    if not isinstance(uid, str) or not isinstance(act_description, str):
        return False

    # Enforce the maximum log size to avoid unbounded memory growth.
    if len(activity_log) >= MAX_LOG_ENTRIES:
        return False

    # Create a record as a tuple (or could be dict for extensibility)
    entry = (uid, act_description)

    # Append the new record
    activity_log.append(entry)
    return True

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     for i in range(1005):
#         success = record_user_action(f"user_{i}", f"action {i}")
#         if not success:
#             print(f"Log limit reached at iteration {i}")