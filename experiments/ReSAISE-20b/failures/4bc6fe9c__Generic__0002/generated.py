import sys
import threading

# Global cache and configuration
user_cache: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()

# Configuration limits (adjust as needed)
_MAX_ITEMS = 1000
_MAX_TOTAL_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def _current_cache_size() -> int:
    """Return the current approximate memory usage of the cache."""
    size = 0
    for uid, data in user_cache.items():
        # Include the key and value sizes
        size += sys.getsizeof(uid) + sys.getsizeof(data)
    return size


def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user information in the global cache.

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
    # Basic validation of inputs
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    with _CACHE_LOCK:
        # If the entry already exists, we allow update but check size constraints
        if uid in user_cache:
            # Remove old entry temporarily to compute new size accurately
            old_entry_size = sys.getsizeof(uid) + sys.getsizeof(user_cache[uid])
        else:
            old_entry_size = 0

        new_entry_size = sys.getsizeof(uid) + sys.getsizeof(data)
        current_size = _current_cache_size() - old_entry_size

        # Check limits
        if len(user_cache) >= _MAX_ITEMS and uid not in user_cache:
            return False
        if current_size + new_entry_size > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Store the data
        user_cache[uid] = data
        return True