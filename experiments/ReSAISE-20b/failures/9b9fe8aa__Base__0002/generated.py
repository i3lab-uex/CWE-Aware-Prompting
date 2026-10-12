import threading

# Global cache dictionary and lock for thread safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Configuration constants for cache limits
_MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024   # 50 MB
_MAX_CACHE_ENTRIES: int = 10_000

def _current_cache_size() -> int:
    """Estimate the memory size of cached entries in bytes."""
    import sys
    total = 0
    for details in user_cache.values():
        # Rough estimate: size of the dict object and its contents
        total += sys.getsizeof(details)
        for key, value in details.items():
            total += sys.getsizeof(key) + sys.getsizeof(value)
    return total

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(user_details, dict):
        return False

    with _user_cache_lock:
        # Enforce entry count limit
        if len(user_cache) >= _MAX_CACHE_ENTRIES and user_identifier not in user_cache:
            return False

        # Estimate new size
        new_entry_size = sys.getsizeof(user_details)
        for key, value in user_details.items():
            new_entry_size += sys.getsizeof(key) + sys.getsizeof(value)

        current_size = _current_cache_size()
        if (current_size + new_entry_size) > _MAX_CACHE_SIZE_BYTES and user_identifier not in user_cache:
            return False

        # Store or update the entry
        user_cache[user_identifier] = user_details.copy()
    return True