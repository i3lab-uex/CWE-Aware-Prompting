import threading
from collections import OrderedDict

# Global cache dictionary implemented as an ordered dict to support LRU eviction
user_cache: "OrderedDict[str, dict]" = OrderedDict()

# Configuration constants
MAX_CACHE_SIZE = 1000          # Maximum number of entries allowed in the cache
CACHE_LOCK = threading.Lock()  # Ensure thread‑safe access to the cache

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user‑specific data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details to cache.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation to avoid corrupting the cache
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    with CACHE_LOCK:
        # Evict least‑recently used item if cache exceeds its maximum size
        if len(user_cache) >= MAX_CACHE_SIZE:
            # Pop the first item (oldest entry)
            user_cache.popitem(last=False)

        # Insert or update the cache entry
        user_cache[client_id] = client_data

    return True