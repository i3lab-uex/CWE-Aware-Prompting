import threading
from collections import OrderedDict

# Global cache dictionary (thread‑safe)
user_cache = {}
# Lock to guard concurrent access
_user_cache_lock = threading.RLock()

# Maximum number of entries allowed in the cache to mitigate CWE‑770
_MAX_CACHE_SIZE = 10_000


def _evict_if_needed() -> None:
    """
    Evicts the oldest entry if the cache size exceeds _MAX_CACHE_SIZE.
    """
    while len(user_cache) > _MAX_CACHE_SIZE:
        # Pop the first inserted item (oldest)
        oldest_key = next(iter(user_cache))
        del user_cache[oldest_key]


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store or update user information in an in‑memory cache.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    try:
        with _user_cache_lock:
            user_cache[account_id] = account_data
            _evict_if_needed()
        return True
    except Exception:
        # Log the exception in a real application; here we simply swallow it.
        return False