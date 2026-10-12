import sys
import threading

# Global cache dictionary and associated lock for thread safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
_MAX_CACHE_SIZE_BYTES: int = 10 * 1024 * 1024      # 10 MB
_MAX_CACHE_ENTRIES: int = 1000

def _current_cache_size() -> int:
    """
    Roughly estimate the current memory usage of user_cache in bytes.
    Uses sys.getsizeof on keys and values; not exact but sufficient for limits.
    """
    size = sys.getsizeof(user_cache)
    for key, value in user_cache.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Cache user information in a global dictionary with size and count limits.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was added or updated successfully; False if adding it would exceed
        configured limits.
    """
    # Basic validation of arguments
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    with _user_cache_lock:
        # Check if adding a new entry would exceed the maximum number of entries
        if client_id not in user_cache and len(user_cache) >= _MAX_CACHE_ENTRIES:
            return False

        # Estimate the new size if this entry is added/updated
        current_size = _current_cache_size()
        # Subtract size of existing entry if present (to avoid double counting)
        old_entry_size = 0
        if client_id in user_cache:
            old_entry_size = sys.getsizeof(client_id) + sys.getsizeof(user_cache[client_id])

        new_entry_size = sys.getsizeof(client_id) + sys.getsizeof(client_data)
        projected_size = current_size - old_entry_size + new_entry_size

        if projected_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Store or update the entry
        user_cache[client_id] = client_data.copy()
        return True