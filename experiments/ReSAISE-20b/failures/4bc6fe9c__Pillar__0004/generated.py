import sys
import threading

# Global cache dictionary and its lock for thread‑safe access.
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()

# Configuration for cache limits
_MAX_ENTRIES: int = 10_000               # Maximum number of cached users
_MAX_TOTAL_BYTES: int = 50 * 1024 * 1024  # Maximum total memory usage (~50 MiB)

def _current_total_bytes() -> int:
    """Return the approximate memory usage of all cached user data."""
    total = 0
    for d in user_cache.values():
        total += sys.getsizeof(d)
        # Roughly add sizes of keys and values inside the dict
        for k, v in d.items():
            total += sys.getsizeof(k)
            total += sys.getsizeof(v)
    return total

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing attributes and details related to the user.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (e.g., size or count limits exceeded).
    """
    # Basic validation
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    # Estimate size of the new entry
    try:
        new_entry_size = sys.getsizeof(data)
        for k, v in data.items():
            new_entry_size += sys.getsizeof(k) + sys.getsizeof(v)
    except Exception:
        # If we cannot estimate size, reject the entry to be safe
        return False

    with _cache_lock:
        # Check if we need to evict entries
        if uid not in user_cache and len(user_cache) >= _MAX_ENTRIES:
            # Simple eviction: remove the oldest entry (FIFO)
            try:
                first_key = next(iter(user_cache))
                del user_cache[first_key]
            except StopIteration:
                pass  # cache is unexpectedly empty

        # Check total size constraint
        if (_current_total_bytes() + new_entry_size) > _MAX_TOTAL_BYTES:
            return False

        # Store the data
        user_cache[uid] = data.copy()  # store a shallow copy to avoid external mutation
        return True