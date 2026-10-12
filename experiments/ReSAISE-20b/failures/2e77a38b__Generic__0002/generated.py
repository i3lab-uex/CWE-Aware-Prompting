import threading
from copy import deepcopy

# Global cache dictionary and a lock for thread safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store user-specific information in a global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the user.
    cust_data : dict
        Dictionary containing the user's data.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    try:
        # Use deepcopy to avoid accidental external mutations
        data_copy = deepcopy(cust_data)

        with _user_cache_lock:
            user_cache[cust_id] = data_copy

        return True
    except Exception:
        # Any unexpected error results in a graceful failure
        return False