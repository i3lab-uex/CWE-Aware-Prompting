import threading

# Global cache dictionary and configuration constants
user_cache = {}
CACHE_MAX_ITEMS = 1000          # maximum number of users that can be cached
CACHE_MAX_SIZE_BYTES = 50 * 1024 * 1024  # maximum total size in bytes (~50 MB)

# Lock to ensure thread‑safe access to the cache
_cache_lock = threading.RLock()


def _current_cache_size() -> int:
    """
    Estimate the current memory footprint of the cached user details.
    Uses `sys.getsizeof` recursively for nested objects.
    """
    import sys

    def sizeof(o, seen=None):
        if seen is None:
            seen = set()
        obj_id = id(o)
        if obj_id in seen:
            return 0
        seen.add(obj_id)
        size = sys.getsizeof(o)

        if isinstance(o, dict):
            size += sum(sizeof(k, seen) + sizeof(v, seen) for k, v in o.items())
        elif isinstance(o, (list, tuple, set, frozenset)):
            size += sum(sizeof(i, seen) for i in o)
        return size

    with _cache_lock:
        total = sum(sizeof(details) for details in user_cache.values())
    return total


def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if caching succeeded, False if it would exceed size or count limits.
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(user_details, dict):
        return False

    # Prepare for caching: estimate size of new entry
    import sys

    def estimate_size(d):
        return sys.getsizeof(d) + sum(sys.getsizeof(k) + sys.getsizeof(v)
                                      for k, v in d.items())

    new_entry_size = estimate_size(user_details)

    with _cache_lock:
        # Enforce maximum item count
        if user_identifier not in user_cache and len(user_cache) >= CACHE_MAX_ITEMS:
            return False

        # Enforce maximum total size
        current_size = _current_cache_size()
        if current_size + new_entry_size > CACHE_MAX_SIZE_BYTES:
            return False

        # Store or update the cache entry
        user_cache[user_identifier] = user_details.copy()  # shallow copy to avoid external mutation

    return True