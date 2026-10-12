import threading

# Global activity log and a lock for thread‑safe access
activity_log: list[dict[str, str]] = []
_activity_lock = threading.Lock()

# Maximum number of entries allowed in the log
_MAX_LOG_ENTRIES = 10_000


def record_user_action(uid: str, act_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    act_description : str
        Textual description of the action performed.

    Returns
    -------
    bool
        True if the entry was added, False if it was rejected due to the log size limit.

    Notes
    -----
    * The function is thread‑safe; concurrent calls are serialized by a lock.
    * No explicit security checks (e.g., authentication) are performed here; callers
      should ensure the caller is authorized to log actions.
    * The function enforces a hard cap on the number of entries to avoid unbounded
      memory growth, mitigating CWE‑664 by ensuring resources are released/limited.
    """
    # Quick sanity checks
    if not isinstance(uid, str) or not isinstance(act_description, str):
        raise TypeError("uid and act_description must be strings")

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_ENTRIES:
            # Log limit reached – do not add the entry
            return False

        # Append a new record; we store a copy to avoid accidental mutation later
        entry = {"uid": uid, "action": act_description}
        activity_log.append(entry)

    return True