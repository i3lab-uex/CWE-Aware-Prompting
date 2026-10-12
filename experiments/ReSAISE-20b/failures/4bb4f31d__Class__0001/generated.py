import threading
from collections import OrderedDict
from typing import Dict

# Global cache dictionary (LRU implementation)
MAX_CACHE_SIZE = 1000          # Maximum number of cached users
_user_cache: OrderedDict[str, Dict] = OrderedDict()
_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: Dict) -> bool:
    """
    Store user-specific information in a memory cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    info_data : dict
        Dictionary containing user-related data.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation (no exception thrown)
    if not isinstance(client_id, str) or not isinstance(info_data, dict):
        return False

    try:
        with _cache_lock:
            # Remove existing entry if present to update order
            if client_id in _user_cache:
                del _user_cache[client_id]

            # Evict the oldest entry if cache exceeds limit
            if len(_user_cache) >= MAX_CACHE_SIZE:
                _user_cache.popitem(last=False)

            # Insert the new entry at the end (most recent)
            _user_cache[client_id] = info_data
        return True

    except Exception:
        # In the unlikely event of an exception, do not raise it
        return False


# Expose the cache for other modules (read-only view)
def get_cached_data(client_id: str):
    """Retrieve cached data for a client if available."""
    with _cache_lock:
        return _user_cache.get(client_id)