import threading
from collections import OrderedDict

# Global cache and its lock for thread‑safety
_user_cache_lock = threading.RLock()
_user_cache: OrderedDict[str, dict] = OrderedDict()

# Maximum number of entries allowed in the cache to avoid uncontrolled resource consumption
_MAX_CACHE_SIZE = 1000

def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Cache user data in memory for quick retrieval.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        A dictionary containing user information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    with _user_cache_lock:
        # Evict least‑recently used entry if cache is full
        if len(_user_cache) >= _MAX_CACHE_SIZE:
            try:
                _user_cache.popitem(last=False)
            except KeyError:
                pass  # cache was empty

        # Store or update the entry
        _user_cache[user_id] = user_data.copy()  # copy to avoid external mutation

    return True