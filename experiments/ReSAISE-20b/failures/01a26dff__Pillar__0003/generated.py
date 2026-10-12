import threading
from copy import deepcopy

# Global cache dictionary and a lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store a copy of user-specific data in the global `user_cache`.

    Parameters
    ----------
    account_id : str
        A unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Validate inputs to avoid corrupting the cache
    if not isinstance(account_id, str) or not account_id:
        return False

    # Only allow mapping types; reject other iterables
    if not isinstance(account_data, dict):
        return False

    try:
        # Use deepcopy to prevent accidental mutation of cached data
        data_copy = deepcopy(account_data)
    except Exception:
        # If deepcopy fails, do not cache
        return False

    with _user_cache_lock:
        try:
            user_cache[account_id] = data_copy
        except Exception:
            # Any exception during assignment indicates failure
            return False

    return True