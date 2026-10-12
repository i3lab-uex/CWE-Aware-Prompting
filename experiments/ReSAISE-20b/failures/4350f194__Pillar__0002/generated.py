import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}

# Lock to ensure thread‑safe access to the cache
_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Store user data in the global cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type checks – avoid raising exceptions
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    try:
        with _cache_lock:
            user_cache[user_id] = user_data.copy()  # store a shallow copy
        return True
    except Exception:
        # If any unexpected error occurs, do not crash; just report failure.
        return False