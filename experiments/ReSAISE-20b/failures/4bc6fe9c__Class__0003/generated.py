import sys
import threading

# Global cache dictionary and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits
_MAX_CACHE_ENTRIES: int = 1_000          # maximum number of cached users
_MAX_CACHE_BYTES: int = 10 * 1024 * 1024 # maximum total size of the cache in bytes (≈10 MiB)

def _current_cache_size() -> int:
    """Return the approximate memory size of all cached data."""
    total = 0
    for value in user_cache.values():
        # Use sys.getsizeof to approximate the memory footprint of each dict
        total += sys.getsizeof(value)
    return total

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific details in the global cache.

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
    # Basic type validation (fails silently)
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    # Ensure the cache does not exceed configured limits
    with _user_cache_lock:
        if uid in user_cache:
            # Update existing entry – size may change
            pass
        else:
            if len(user_cache) >= _MAX_CACHE_ENTRIES:
                return False

        # Estimate new size if this entry were added/updated
        new_size = _current_cache_size()
        # Subtract size of existing entry if present
        if uid in user_cache:
            new_size -= sys.getsizeof(user_cache[uid])

        # Add size of the new data
        new_size += sys.getsizeof(data)

        if new_size > _MAX_CACHE_BYTES:
            return False

        # Store the data
        user_cache[uid] = data.copy()  # shallow copy to avoid accidental external mutation

    return True