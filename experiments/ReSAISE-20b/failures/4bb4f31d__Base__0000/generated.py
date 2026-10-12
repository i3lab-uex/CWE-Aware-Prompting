import threading
from collections import OrderedDict

# Global cache: maps client_id -> info_data
user_cache = OrderedDict()
# Maximum number of entries allowed in the cache to avoid unbounded growth
_MAX_CACHE_SIZE = 1000

# Lock to make cache thread‑safe in concurrent environments
_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user‑specific information in a global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    info_data : dict
        Dictionary containing user‑related data to cache.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    try:
        with _cache_lock:
            # If client_id already exists, remove it to update order
            if client_id in user_cache:
                del user_cache[client_id]

            # Evict least‑recently used entry if cache is full
            if len(user_cache) >= _MAX_CACHE_SIZE:
                # popitem(last=False) removes the first item (LRU)
                user_cache.popitem(last=False)

            # Insert new entry
            user_cache[client_id] = info_data

        return True
    except Exception:
        # No exception should propagate; just indicate failure
        return False