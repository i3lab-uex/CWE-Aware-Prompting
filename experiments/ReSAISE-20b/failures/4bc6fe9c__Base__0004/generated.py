import sys
import threading

# Global cache dictionary
user_cache = {}
# Lock for thread‑safety
_user_cache_lock = threading.Lock()

# Configuration limits (can be tuned as needed)
_MAX_ENTRIES = 10_000          # Maximum number of cached users
_MAX_CACHE_BYTES = 100 * 1024 * 1024   # 100 MB max cache size

def _current_cache_size() -> int:
    """Return the approximate current memory usage of the cache in bytes."""
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for a user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was stored successfully; False if adding it would
        exceed the configured limits.
    """
    # Basic validation of inputs
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    with _user_cache_lock:
        # If the entry already exists, we can overwrite without size check
        if uid in user_cache:
            user_cache[uid] = data
            return True

        # Enforce entry count limit
        if len(user_cache) >= _MAX_ENTRIES:
            return False

        # Estimate the size impact of adding this entry
        new_entry_size = sys.getsizeof(uid) + sys.getsizeof(data)
        if _current_cache_size() + new_entry_size > _MAX_CACHE_BYTES:
            return False

        # Store the entry
        user_cache[uid] = data
        return True