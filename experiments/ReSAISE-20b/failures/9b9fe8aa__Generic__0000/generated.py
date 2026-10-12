import sys
import threading

# Global cache dictionary and configuration limits
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration constants
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024          # 10 MB total cache size
_MAX_CACHE_ENTRIES = 1000                        # Maximum number of cached users


def _current_cache_size() -> int:
    """
    Estimate the current cache size in bytes by summing the sizes of
    keys and values.  This is a heuristic; it may not reflect the exact
    memory usage but provides a reasonable bound.
    """
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size


def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Cache the provided `user_details` under the given `user_identifier`.

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the cache entry was added or updated successfully,
        False if adding it would exceed configured size or count limits.
    """
    # Basic validation of arguments
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    with _user_cache_lock:
        # If the user is already cached, update without size checks
        if user_identifier in user_cache:
            user_cache[user_identifier] = user_details
            return True

        # Check entry count limit
        if len(user_cache) >= _MAX_CACHE_ENTRIES:
            return False

        # Estimate size of the new entry
        entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)

        # Check size limit
        if _current_cache_size() + entry_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Store the new entry
        user_cache[user_identifier] = user_details
        return True