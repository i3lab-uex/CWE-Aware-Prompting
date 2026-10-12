import sys
import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()

# Configuration limits
_MAX_ENTRIES: int = 10_000          # maximum number of cached users
_MAX_CACHE_BYTES: int = 10 * 1024**2   # ~10 MiB total size

def _estimate_dict_size(d: dict) -> int:
    """Return an approximate memory footprint of a dictionary."""
    size = sys.getsizeof(d)
    for k, v in d.items():
        size += sys.getsizeof(k) + sys.getsizeof(v)
    return size

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store a client's data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client.
    client_data : dict
        Dictionary containing client attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    # Estimate size of new entry
    entry_size = _estimate_dict_size(client_data)

    with _cache_lock:
        # If key already exists, replace it – size adjustment handled below
        current_size = sum(_estimate_dict_size(v) for v in user_cache.values())
        new_total_size = current_size - _estimate_dict_size(user_cache.get(client_id, {})) + entry_size

        # Check against limits
        if len(user_cache) >= _MAX_ENTRIES and client_id not in user_cache:
            return False
        if new_total_size > _MAX_CACHE_BYTES:
            # Attempt to evict least recently used entries (simple FIFO eviction)
            while new_total_size > _MAX_CACHE_BYTES and user_cache:
                oldest_key = next(iter(user_cache))
                old_size = _estimate_dict_size(user_cache.pop(oldest_key))
                new_total_size -= old_size
            if new_total_size > _MAX_CACHE_BYTES:
                # Still too large after eviction – abort
                return False

        # Cache the data (overwrites if key exists)
        user_cache[client_id] = client_data.copy()
    return True