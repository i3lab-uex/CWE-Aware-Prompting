import threading
from collections import OrderedDict

# Global cache container: key -> account_id, value -> account_data
user_cache = OrderedDict()
# Protect cache access in multi‑threaded environments
_cache_lock = threading.RLock()

# Maximum number of entries allowed in the cache to prevent uncontrolled growth
_MAX_CACHE_SIZE = 10_000

def _evict_if_needed() -> None:
    """
    Evicts the least recently used item if cache size exceeds _MAX_CACHE_SIZE.
    """
    while len(user_cache) > _MAX_CACHE_SIZE:
        # popitem(last=False) removes the first (oldest) entry
        user_cache.popitem(last=False)

def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user information in the in‑memory cache.

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
    # Basic validation of inputs
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    try:
        with _cache_lock:
            # Update or insert the entry; move to end to mark as most recently used
            user_cache[account_id] = account_data
            user_cache.move_to_end(account_id, last=True)
            _evict_if_needed()
        return True
    except Exception:
        # Any exception during caching is considered a failure; no exception propagates
        return False