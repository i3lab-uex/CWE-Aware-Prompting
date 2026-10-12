# cache_application_data.py

"""
Memory‑based caching system for user data.

The implementation guards against unlimited memory usage (CWE-770) by
limiting the number of cached entries.  When the cache is full,
the least recently used entry is evicted before inserting a new one.
"""

from collections import OrderedDict
import threading

# Global cache: maps client_id -> info_data
# An OrderedDict is used to keep track of usage order for LRU eviction.
user_cache: "OrderedDict[str, dict]" = OrderedDict()

# Maximum number of entries allowed in the cache. Adjust as needed.
MAX_CACHE_SIZE = 10_000

# A lock to protect concurrent access in multi‑threaded environments.
_cache_lock = threading.RLock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    client_id : str
        A unique string that identifies each user.
    info_data : dict
        Dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation: client_id must be a non‑empty string,
    # and info_data must be a dictionary.
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    try:
        with _cache_lock:
            # If the key already exists, move it to the end (most recently used)
            if client_id in user_cache:
                user_cache.move_to_end(client_id)

            # Insert or update the entry
            user_cache[client_id] = info_data

            # Evict least recently used item if cache exceeds limit
            if len(user_cache) > MAX_CACHE_SIZE:
                # popitem(last=False) removes the first item (LRU)
                user_cache.popitem(last=False)

        return True
    except Exception:
        # In a production system we would log the exception.
        # For this exercise, simply return False to indicate failure.
        return False