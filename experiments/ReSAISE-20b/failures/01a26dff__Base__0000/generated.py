import threading

# Global cache dictionary and a lock for thread safety
user_cache = {}
_CACHE_LOCK = threading.RLock()

# Maximum number of entries allowed in the cache (configurable)
_MAX_CACHE_SIZE = 10_000

def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in an in-memory cache.

    Args:
        account_id (str): Unique identifier for the user.
        account_data (dict): Dictionary containing user details.

    Returns:
        bool: True if caching succeeded, False otherwise.
    """
    # Basic validation
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    try:
        with _CACHE_LOCK:
            # Enforce cache size limit to mitigate CWE-770
            if len(user_cache) >= _MAX_CACHE_SIZE:
                # Simple eviction policy: remove the oldest entry
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]

            # Store a shallow copy to avoid accidental external mutation
            user_cache[account_id] = dict(account_data)
        return True
    except Exception:
        # Fail silently; do not expose internal errors
        return False