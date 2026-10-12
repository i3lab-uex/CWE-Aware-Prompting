import threading

# Global activity log and its lock for thread‑safety
activity_log: list[dict] = []
_activity_lock = threading.Lock()

# Optional maximum number of entries to prevent uncontrolled growth
_MAX_LOG_SIZE: int = 10_000


def save_user_interaction(user_alias: str, interaction_desc: str) -> bool:
    """
    Record a user action in the global activity log.

    Parameters
    ----------
    user_alias : str
        A unique identifier for the user who performed the action.
    interaction_desc : str
        A textual description of the action taken by the user.

    Returns
    -------
    bool
        True if the log entry was successfully added, False if the
        operation failed due to exceeding the configured maximum size.

    Notes
    -----
    * The function uses a global lock to ensure atomicity and avoid race
      conditions in multi‑threaded environments.
    * The log size is capped to prevent uncontrolled resource consumption
      (CWE‑664).
    """
    # Basic validation: reject empty or whitespace only values
    if not user_alias.strip() or not interaction_desc.strip():
        return False

    with _activity_lock:
        if len(activity_log) >= _MAX_LOG_SIZE:
            # Do not add the entry; log has reached its limit
            return False

        # Append a new record with a timestamp for audit purposes
        activity_log.append(
            {
                "user_alias": user_alias,
                "interaction_desc": interaction_desc,
                # Use UTC timestamp to avoid timezone issues
                "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            }
        )
    return True