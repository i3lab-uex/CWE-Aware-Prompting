import threading

# Global cache with a maximum size to mitigate CWE-770 (unbounded resource allocation)
MAX_CACHE_SIZE = 10_000          # Adjust as appropriate for your environment
_user_cache_lock = threading.Lock()
user_cache: dict[str, dict] = {}

def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Cache user data in memory for quick access.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        A dictionary containing user information.

    Returns
    -------
    bool
        True if caching was successful, False otherwise.
    """
    # Basic validation: ensure user_id is a non-empty string
    if not isinstance(user_id, str) or not user_id:
        return False

    # Ensure user_data is a dictionary
    if not isinstance(user_data, dict):
        return False

    with _user_cache_lock:
        # If the cache is at capacity, evict an arbitrary entry (FIFO)
        if len(user_cache) >= MAX_CACHE_SIZE:
            # Remove the first inserted item (simple FIFO eviction)
            try:
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]
            except StopIteration:
                # Cache is unexpectedly empty; nothing to evict
                pass

        # Store or update the user data
        try:
            user_cache[user_id] = user_data.copy()
            return True
        except Exception:
            # Any unexpected error during caching results in a failure flag
            return False