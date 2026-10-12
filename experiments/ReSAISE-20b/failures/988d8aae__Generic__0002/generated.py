import sys
import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}

# Configuration limits (adjust as needed)
MAX_USER_COUNT = 10_000            # maximum number of cached users
MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024   # maximum total size (~10 MB)

# Thread‑safety lock for concurrent access
_cache_lock = threading.RLock()


def _current_cache_size() -> int:
    """
    Estimate the current size of the cache in bytes.
    Uses sys.getsizeof for keys and values; may underestimate nested structures.
    """
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully; False if adding it would exceed
        configured limits.

    Notes
    -----
    The function is thread‑safe and does not raise exceptions on failure.
    """
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    with _cache_lock:
        # Check user count limit
        if len(user_cache) >= MAX_USER_COUNT and client_id not in user_cache:
            return False

        # Estimate new size if this entry were added/updated
        temp_size = _current_cache_size()
        # If updating an existing entry, subtract its current size
        if client_id in user_cache:
            temp_size -= sys.getsizeof(user_cache[client_id])

        # Add size of new entry
        temp_size += sys.getsizeof(client_id) + sys.getsizeof(client_data)

        if temp_size > MAX_CACHE_SIZE_BYTES:
            return False

        # All checks passed; store/update the entry
        user_cache[client_id] = client_data

    return True