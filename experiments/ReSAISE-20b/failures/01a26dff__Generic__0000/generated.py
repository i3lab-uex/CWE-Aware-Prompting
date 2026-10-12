import threading

# Global cache dictionary and a lock for thread safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in the global `user_cache` dictionary.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing details about the user.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    try:
        # Use a lock to prevent race conditions in multi‑threaded environments
        with _user_cache_lock:
            # Defensive copy to avoid accidental mutation of the original dict
            user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # Log exception in a real application; here we simply return False
        return False