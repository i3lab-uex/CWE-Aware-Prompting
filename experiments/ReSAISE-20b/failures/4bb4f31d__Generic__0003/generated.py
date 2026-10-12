import threading

# Global cache dictionary and a lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Stores user‑specific information in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    info_data : dict
        Dictionary containing arbitrary user data to cache.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type validation to guard against accidental misuse
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    try:
        # Use a re‑entrant lock to protect concurrent writes
        with _user_cache_lock:
            user_cache[client_id] = info_data.copy()
        return True
    except Exception:
        # In a real system we might log the exception; here we simply signal failure
        return False