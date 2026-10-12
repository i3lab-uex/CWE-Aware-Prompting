import threading
import copy

# Global cache dictionary and a lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in the global cache.

    Parameters
    ----------
    account_id : str
        Unique identifier for a user.
    account_data : dict
        Dictionary containing the user's data.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation
    if not isinstance(account_id, str) or not isinstance(account_data, dict):
        return False

    try:
        # Use a deep copy to prevent external mutation of cached data
        data_copy = copy.deepcopy(account_data)

        with _cache_lock:
            user_cache[account_id] = data_copy

        return True
    except Exception:
        # Any unexpected error (e.g., memory issues) results in a failure
        return False