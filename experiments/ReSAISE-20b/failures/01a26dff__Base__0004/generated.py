import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Maximum number of cached accounts to mitigate CWE‑770
_MAX_CACHE_SIZE: int = 10_000


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the cache entry was stored successfully,
        False otherwise (e.g., if account_id is empty or
        the cache size limit is reached).
    """
    # Basic validation of input
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    with _cache_lock:
        # Enforce a maximum cache size to avoid unlimited memory growth
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Optionally, evict the oldest entry (simple FIFO)
            try:
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]
            except StopIteration:
                return False

        # Store the data
        user_cache[account_id] = account_data.copy()
    return True