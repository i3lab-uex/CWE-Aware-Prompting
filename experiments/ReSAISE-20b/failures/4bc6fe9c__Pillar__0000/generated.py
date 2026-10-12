import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Configuration limits (can be adjusted as needed)
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024   # 10 MB
_MAX_CACHE_ENTRIES = 1000

def _current_cache_size() -> int:
    """Estimate the current cache size in bytes."""
    return sum(len(str(k).encode('utf-8')) + len(str(v).encode('utf-8'))
               for k, v in user_cache.items())

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    with _cache_lock:
        # Enforce entry limit
        if len(user_cache) >= _MAX_CACHE_ENTRIES and uid not in user_cache:
            return False

        # Estimate new size after insertion
        tentative_size = _current_cache_size()
        tentative_size += len(uid.encode('utf-8'))
        tentative_size += sum(len(str(k).encode('utf-8')) + len(str(v).encode('utf-8'))
                              for k, v in data.items())

        if tentative_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Store or update the entry
        user_cache[uid] = data.copy()  # shallow copy to avoid external mutation

    return True