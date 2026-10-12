import threading

# Global cache dictionary and a lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user information in the in‑memory cache.

    Args:
        account_id (str): Unique identifier for the user.
        account_data (dict): Dictionary containing user details.

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    try:
        # Validate input types
        if not isinstance(account_id, str) or not isinstance(account_data, dict):
            return False

        # Thread‑safe write to the cache
        with _cache_lock:
            user_cache[account_id] = account_data.copy()  # store a shallow copy

        return True
    except Exception:
        # In case of any unexpected error, do not crash the application
        return False