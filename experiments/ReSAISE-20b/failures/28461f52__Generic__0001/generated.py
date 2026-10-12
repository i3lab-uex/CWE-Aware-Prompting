import threading

# Global activity log list and its lock for thread‑safe access.
activity_log: list[dict[str, str]] = []
_activity_lock = threading.Lock()

# Optional configuration – maximum number of log entries that can be stored.
MAX_LOG_ENTRIES: int = 100_000


def track_user_event(user_name: str, event_description: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_name : str
        Unique identifier for the user.
    event_description : str
        Human‑readable description of the action.

    Returns
    -------
    bool
        ``True`` if the entry was added, ``False`` if the log has reached
        :data:`MAX_LOG_ENTRIES`.

    Notes
    -----
    * The function is thread‑safe; multiple threads can call it concurrently.
    * It performs minimal validation: ensures both arguments are strings and
      not empty.  More elaborate checks (e.g., length limits, escaping) can
      be added as needed.
    """
    # Basic validation – ensure non‑empty strings to avoid meaningless log entries
    if not isinstance(user_name, str) or not isinstance(event_description, str):
        return False
    if not user_name.strip() or not event_description.strip():
        return False

    with _activity_lock:
        # Check if we have reached the configured limit
        if len(activity_log) >= MAX_LOG_ENTRIES:
            return False

        # Append the new event as a dictionary for clarity
        activity_log.append(
            {
                "user": user_name.strip(),
                "event": event_description.strip(),
            }
        )
    return True