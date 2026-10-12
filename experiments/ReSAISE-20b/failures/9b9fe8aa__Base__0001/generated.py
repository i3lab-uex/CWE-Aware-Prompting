import sys
import threading

# Global cache dictionary
user_cache = {}
# Lock to make the cache thread‑safe
_cache_lock = threading.Lock()

# Configuration: limits for total size (bytes) and maximum number of entries
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024   # 10 MB
_MAX_CACHE_ENTRIES = 10000                # arbitrary limit

def _current_cache_size() -> int:
    """Return the current approximate size of the cache in bytes."""
    total = 0
    for key, value in user_cache.items():
        total += sys.getsizeof(key) + sys.getsizeof(value)
    return total

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store a user's details in the global cache.

    Parameters
    ----------
    user_identifier : str
        A unique string identifier for the user.
    user_details : dict
        Dictionary containing attributes related to the user.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (size or count limit reached).
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    with _cache_lock:
        # Check if entry already exists; update size accordingly
        old_entry_size = 0
        if user_identifier in user_cache:
            old_entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_cache[user_identifier])

        new_entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)

        # Calculate prospective cache size
        current_size = _current_cache_size()
        new_total_size = current_size - old_entry_size + new_entry_size

        # Enforce size and count limits
        if (len(user_cache) + 1 > _MAX_CACHE_ENTRIES) or (new_total_size > _MAX_CACHE_SIZE_BYTES):
            return False

        # Insert/Update the cache entry
        user_cache[user_identifier] = user_details
    return True