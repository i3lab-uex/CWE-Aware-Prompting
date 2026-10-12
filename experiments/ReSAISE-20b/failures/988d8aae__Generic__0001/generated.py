import sys
import threading

# Global cache dictionary and configuration limits
user_cache: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()

# Maximum allowed total size of all cached data (bytes) and maximum number of entries
_MAX_CACHE_SIZE = 10 * 1024 * 1024   # 10 MB
_MAX_ENTRIES = 1000

def _current_cache_size() -> int:
    """Return the current approximate size of all cached values in bytes."""
    return sum(sys.getsizeof(v) for v in user_cache.values())

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    client_id : str
        A unique string identifier for the user.
    client_data : dict
        Dictionary containing user attributes and details.

    Returns
    -------
    bool
        True if the caching operation succeeds, False otherwise.
    """
    # Quick sanity checks on inputs
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    # Calculate the size of the new entry
    entry_size = sys.getsizeof(client_data)

    with _CACHE_LOCK:
        # Check count limit
        if len(user_cache) >= _MAX_ENTRIES and client_id not in user_cache:
            return False

        # Check size limit (allow replacement of existing entry without extra cost)
        current_size = _current_cache_size()
        # If the key exists, subtract its size before adding new
        if client_id in user_cache:
            current_size -= sys.getsizeof(user_cache[client_id])

        if current_size + entry_size > _MAX_CACHE_SIZE:
            return False

        # Perform the caching operation
        user_cache[client_id] = client_data.copy()  # store a shallow copy to avoid accidental mutation

    return True