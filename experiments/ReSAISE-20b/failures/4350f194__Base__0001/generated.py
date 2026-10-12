import threading

# Global cache dictionary and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache (CWE‑770 mitigation)
_MAX_CACHE_SIZE = 10_000


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Store user data in an in‑memory cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False if the cache is full.
    """
    # Basic validation
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    with _cache_lock:
        # Check cache size limit
        if len(user_cache) >= _MAX_CACHE_SIZE:
            return False

        user_cache[user_id] = user_data
        return True