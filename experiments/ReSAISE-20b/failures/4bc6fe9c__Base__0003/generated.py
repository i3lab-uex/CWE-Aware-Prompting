import threading

# Global cache and its configuration
user_cache = {}
_cache_lock = threading.Lock()

# Configuration constants (adjust as needed)
_MAX_CACHE_SIZE_BYTES = 50 * 1024 * 1024   # 50 MB total
_MAX_CACHE_ENTRIES = 1000                  # maximum number of users cached

def _current_cache_size() -> int:
    """
    Estimate the current cache size in bytes by summing
    the sizes of all stored data objects.
    """
    total = 0
    for value in user_cache.values():
        # Rough estimate: use sys.getsizeof on the dict itself
        import sys
        total += sys.getsizeof(value)
    return total

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for a user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was stored successfully,
        False if adding it would exceed size or count limits.
    """
    # Basic input validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    with _cache_lock:
        # If the entry already exists, we replace it but still respect limits
        if uid in user_cache:
            # Temporarily remove old entry to recalculate size
            del user_cache[uid]

        current_size = _current_cache_size()
        # Estimate size of new entry
        import sys
        entry_size = sys.getsizeof(data)

        # Check against size limit
        if current_size + entry_size > _MAX_CACHE_SIZE_BYTES:
            # Re-insert old data if we removed it
            if uid in user_cache:
                user_cache[uid] = data  # restore (though we deleted above)
            return False

        # Check against count limit
        if len(user_cache) + 1 > _MAX_CACHE_ENTRIES:
            # Re-insert old data if we removed it
            if uid in user_cache:
                user_cache[uid] = data
            return False

        # Store the new entry
        user_cache[uid] = data
        return True