import threading
from collections import OrderedDict

# Global cache dictionary with a maximum size and count limit
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024          # 10 MB
_MAX_CACHE_ENTRIES = 1000                        # maximum number of entries

# OrderedDict preserves insertion order for simple LRU eviction
user_cache = OrderedDict()
_user_cache_lock = threading.Lock()


def _current_cache_size() -> int:
    """
    Estimate the current memory usage of the cache in bytes.
    This is a heuristic based on the size of keys and values.
    """
    total = 0
    for key, value in user_cache.items():
        # Rough size estimation: sys.getsizeof is used as a proxy
        try:
            import sys
            total += sys.getsizeof(key) + sys.getsizeof(value)
        except Exception:
            # Fallback: assume a minimal size if getsizeof fails
            total += 64
    return total


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

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

    with _user_cache_lock:
        # If the entry already exists, update it and move to end (most recently used)
        if client_id in user_cache:
            user_cache.move_to_end(client_id)
            user_cache[client_id] = client_data
        else:
            # Evict least recently used items if limits exceeded
            while (len(user_cache) >= _MAX_CACHE_ENTRIES or
                   _current_cache_size() + sys.getsizeof(client_id) +
                   sum(sys.getsizeof(v) for v in client_data.values()) > _MAX_CACHE_SIZE_BYTES):
                try:
                    # Pop the oldest item
                    user_cache.popitem(last=False)
                except KeyError:
                    break  # nothing to evict

            user_cache[client_id] = client_data
        return True