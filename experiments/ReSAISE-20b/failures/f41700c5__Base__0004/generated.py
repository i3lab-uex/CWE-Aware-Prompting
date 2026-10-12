import threading

# Global cache dictionary and a lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Maximum number of entries allowed in the cache (CWE‑770 mitigation)
_MAX_CACHE_SIZE = 10_000

def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Stores user information in a global cache.

    Parameters
    ----------
    identifier : str
        Unique identifier for the user.
    data_info : dict
        Dictionary containing user‑specific information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid storing empty or non‑dict data
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(data_info, dict):
        return False

    with _user_cache_lock:
        # Enforce cache size limit
        if len(user_cache) >= _MAX_CACHE_SIZE and identifier not in user_cache:
            # Optional: Evict the oldest entry (simple FIFO) to make room
            try:
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]
            except StopIteration:
                # Cache is unexpectedly empty; just fail
                return False

        # Store or update the entry
        user_cache[identifier] = data_info.copy()
    return True