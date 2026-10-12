# cache_client_data.py

"""
In‑memory user data caching module.

The implementation protects against uncontrolled growth (CWE‑770) by enforcing
a configurable maximum number of cached entries. When the cache is full,
the least recently used (LRU) entry is evicted before adding a new one.
"""

from collections import OrderedDict
import threading

# Global cache dictionary (thread‑safe)
user_cache = OrderedDict()
cache_lock = threading.Lock()

# Configuration: maximum number of cached users
MAX_CACHE_SIZE = 10_000

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation: client_id must be a non‑empty string
    if not isinstance(client_id, str) or not client_id:
        return False

    # Basic validation: client_data must be a dictionary
    if not isinstance(client_data, dict):
        return False

    with cache_lock:
        # If the client_id already exists, update and move to end
        if client_id in user_cache:
            user_cache.move_to_end(client_id)
            user_cache[client_id] = client_data
            return True

        # Enforce maximum cache size: evict LRU entry if needed
        if len(user_cache) >= MAX_CACHE_SIZE:
            # popitem(last=False) removes the first (LRU) item
            user_cache.popitem(last=False)

        # Insert new entry
        user_cache[client_id] = client_data

    return True