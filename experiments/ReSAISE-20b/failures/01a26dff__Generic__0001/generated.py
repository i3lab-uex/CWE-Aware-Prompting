import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user information in the global `user_cache`.

    Parameters
    ----------
    account_id : str
        A unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation to avoid corrupting the cache
    if not isinstance(account_id, str) or not isinstance(account_data, dict):
        return False

    try:
        with _user_cache_lock:
            user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # In a real application we might log the exception.
        return False