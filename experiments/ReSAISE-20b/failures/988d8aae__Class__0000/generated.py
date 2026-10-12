import sys
from threading import Lock

# Global cache dictionary and its lock for thread safety
user_cache: dict[str, dict] = {}
_cache_lock = Lock()

# Configuration constants – adjust as needed
MAX_CLIENTS: int = 10_000          # maximum number of cached users
MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB total cache size

def _current_cache_size() -> int:
    """Return the approximate memory footprint of the current cache."""
    size = 0
    for data in user_cache.values():
        size += sys.getsizeof(data)
    return size

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store or update a client's information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the client was cached successfully, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    # Estimate size of the new entry
    entry_size = sys.getsizeof(client_data)

    with _cache_lock:
        # If the client already exists, remove its size contribution
        if client_id in user_cache:
            entry_size -= sys.getsizeof(user_cache[client_id])

        # Enforce client count limit
        if len(user_cache) >= MAX_CLIENTS and client_id not in user_cache:
            return False

        # Enforce total size limit
        current_size = _current_cache_size()
        if current_size + entry_size > MAX_CACHE_SIZE_BYTES and client_id not in user_cache:
            return False

        # Update the cache
        user_cache[client_id] = client_data.copy()  # shallow copy to avoid accidental mutation

    return True