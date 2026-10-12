import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Optional maximum number of cached entries to mitigate CWE‑400
_MAX_CACHE_SIZE = 10_000

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
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to prevent accidental misuse
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    with _user_cache_lock:
        # Enforce cache size limit to avoid uncontrolled growth
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Simple eviction strategy: remove an arbitrary item
            try:
                user_cache.pop(next(iter(user_cache)))
            except StopIteration:
                pass  # cache was empty; unlikely but safe

        try:
            user_cache[account_id] = account_data.copy()
        except Exception:
            # Any unexpected error results in a failure flag
            return False

    return True