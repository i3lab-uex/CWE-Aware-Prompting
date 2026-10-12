import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}
# Lock to ensure thread‑safe access to the cache
_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Stores user-specific data in the global `user_cache`.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing details about the user.

    Returns
    -------
    bool
        True if the caching operation succeeded, False otherwise.
    """
    # Basic type checks – return False instead of raising an exception
    if not isinstance(account_id, str) or not isinstance(account_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # Any unexpected error results in a failure flag
        return False