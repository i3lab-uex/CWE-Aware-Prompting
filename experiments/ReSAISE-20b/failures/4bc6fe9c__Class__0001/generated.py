import sys
import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}
# Lock for thread‑safety
_cache_lock = threading.RLock()

# Configuration limits
_MAX_ENTRIES: int = 10_000            # maximum number of cached users
_MAX_CACHE_SIZE_BYTES: int = 10 * 1024 * 1024  # ~10 MiB total cache size

# Current cache statistics
_current_cache_size_bytes: int = 0


def _estimate_dict_size(d: dict) -> int:
    """
    Estimate the memory footprint of a dictionary in bytes.
    Uses sys.getsizeof recursively on keys and values.
    """
    size = sys.getsizeof(d)
    for k, v in d.items():
        size += sys.getsizeof(k) + sys.getsizeof(v)
    return size


def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific information in a memory‑based cache.

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
    global _current_cache_size_bytes

    # Basic validation
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    # Estimate size of new entry
    new_entry_size = _estimate_dict_size(data)

    with _cache_lock:
        # If entry already exists, adjust size difference
        old_entry_size = 0
        if uid in user_cache:
            old_entry_size = _estimate_dict_size(user_cache[uid])

        # Check entry count limit
        if uid not in user_cache and len(user_cache) >= _MAX_ENTRIES:
            return False

        # Check cache size limit
        projected_size = _current_cache_size_bytes - old_entry_size + new_entry_size
        if projected_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Update cache and statistics
        user_cache[uid] = data
        _current_cache_size_bytes = projected_size

    return True