import sys
import threading

# Global cache and configuration limits
user_cache: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()

# Maximum number of cached entries
_MAX_ENTRIES: int = 10_000

# Approximate maximum memory usage for the cache (bytes)
_MAX_CACHE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB

def _current_cache_size() -> int:
    """Return the current estimated memory size of `user_cache` in bytes."""
    total = 0
    for key, value in user_cache.items():
        total += sys.getsizeof(key)
        total += sys.getsizeof(value)
    return total

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store or update a client's information in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client.
    client_data : dict
        Dictionary containing client attributes.

    Returns
    -------
    bool
        ``True`` if the cache entry was added/updated successfully,
        ``False`` if adding it would exceed size or count limits.
    """
    # Basic type validation
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    with _CACHE_LOCK:
        # Determine if this is a new entry
        is_new_entry = client_id not in user_cache

        # Estimate the size impact of this operation
        new_entry_size = sys.getsizeof(client_id) + sys.getsizeof(client_data)
        current_size = _current_cache_size()

        # If new entry, check count limit
        if is_new_entry and len(user_cache) >= _MAX_ENTRIES:
            return False

        # If new entry, check size limit
        if is_new_entry and (current_size + new_entry_size) > _MAX_CACHE_SIZE_BYTES:
            return False

        # For updates, we simply replace; size may decrease or increase
        if not is_new_entry:
            # Subtract old entry size
            old_size = sys.getsizeof(client_id) + sys.getsizeof(user_cache[client_id])
            if (current_size - old_size + new_entry_size) > _MAX_CACHE_SIZE_BYTES:
                return False

        # Store or update the entry
        user_cache[client_id] = client_data.copy()  # shallow copy to avoid external mutation

        return True