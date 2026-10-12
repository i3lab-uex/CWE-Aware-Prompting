import sys
import threading

# Global cache and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
_MAX_ENTRIES: int = 10_000               # maximum number of cached users
_MAX_CACHE_SIZE_BYTES: int = 10 * 1024 * 1024  # maximum total memory usage (~10 MiB)

def _current_cache_size() -> int:
    """Return the approximate memory usage of the cache in bytes."""
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user information in the global `user_cache`.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully; False if the cache would exceed
        configured limits.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; the caller should check the return value.
    """
    if not isinstance(uid, str) or not isinstance(data, dict):
        # Invalid input; reject silently.
        return False

    with _cache_lock:
        # If the key already exists, treat it as an update – size may change.
        current_size = _current_cache_size()
        if uid in user_cache:
            # Remove old entry size
            current_size -= sys.getsizeof(uid)
            current_size -= sys.getsizeof(user_cache[uid])
        else:
            # New entry: check entry count
            if len(user_cache) >= _MAX_ENTRIES:
                return False

        # Estimate new size
        entry_size = sys.getsizeof(uid) + sys.getsizeof(data)
        if current_size + entry_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # All checks passed – store the data
        user_cache[uid] = data
        return True