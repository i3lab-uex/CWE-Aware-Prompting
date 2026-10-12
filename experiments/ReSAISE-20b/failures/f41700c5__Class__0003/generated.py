import threading
from collections import OrderedDict

# Global cache and lock for thread‑safety
user_cache: OrderedDict[str, dict] = OrderedDict()
cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache
MAX_CACHE_SIZE: int = 1000


def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        Unique string that identifies a user.
    data_info : dict
        Dictionary containing user-related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(data_info, dict):
        return False

    with cache_lock:
        # If the user is already cached, update their position
        if identifier in user_cache:
            user_cache.pop(identifier)

        # Insert the new entry at the end (most recent)
        user_cache[identifier] = data_info

        # Evict least‑recently used entry if cache exceeds maximum size
        if len(user_cache) > MAX_CACHE_SIZE:
            # popitem(last=False) removes the first item inserted (LRU)
            user_cache.popitem(last=False)

    return True