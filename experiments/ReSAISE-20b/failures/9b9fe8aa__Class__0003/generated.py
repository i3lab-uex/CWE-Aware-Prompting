import threading

# Global cache dictionary protected by a lock for thread safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()

# Define maximum cache limits
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024      # 10 MB
_MAX_CACHE_COUNT = 1000                       # maximum number of users cached

def _current_cache_size() -> int:
    """
    Estimate the current size in bytes of all cached user details.
    This uses sys.getsizeof on each dict and its contents recursively.
    """
    import sys
    size = 0
    for user_dict in user_cache.values():
        size += sys.getsizeof(user_dict)
        for key, value in user_dict.items():
            size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store the provided `user_details` in the global cache under
    `user_identifier`.  The function respects defined limits on both
    total number of cached users and estimated memory consumption.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary of attributes related to the user.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    with _cache_lock:
        # If the user is already cached, replace it (count unchanged)
        if user_identifier in user_cache:
            user_cache[user_identifier] = user_details
            return True

        # Check count limit
        if len(user_cache) >= _MAX_CACHE_COUNT:
            return False

        # Estimate new size and enforce size limit
        estimated_size = _current_cache_size() + sys.getsizeof(user_details)
        for key, value in user_details.items():
            estimated_size += sys.getsizeof(key) + sys.getsizeof(value)

        if estimated_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Add to cache
        user_cache[user_identifier] = user_details
        return True