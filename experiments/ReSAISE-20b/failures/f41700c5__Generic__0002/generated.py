import threading

# Global cache dictionary for user data
user_cache: dict[str, dict] = {}

# Lock to ensure thread‑safe access to the cache
_cache_lock = threading.Lock()


def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        A dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation to avoid storing invalid entries
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(data_info, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to prevent external mutation
            user_cache[identifier] = dict(data_info)
        return True
    except Exception:
        # In case of any unforeseen error, do not cache the data
        return False