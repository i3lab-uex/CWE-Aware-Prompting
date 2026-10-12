# cache_client_data.py

from collections import OrderedDict
import threading

# Global cache with a maximum size to mitigate CWE-770 (unbounded allocation)
_MAX_CACHE_SIZE = 1000

# OrderedDict preserves insertion order, enabling simple LRU eviction
_user_cache: "OrderedDict[str, dict]" = OrderedDict()

# Lock to make cache thread‑safe
_cache_lock = threading.RLock()


def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store or update a client's data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the client.
    client_data : dict
        User‑specific information to cache.

    Returns
    -------
    bool
        ``True`` if the data was successfully cached, ``False`` otherwise.

    Notes
    -----
    * The cache has a hard limit of ``_MAX_CACHE_SIZE`` entries. When the limit is
      reached, the least‑recently used entry is evicted.
    * The function performs basic validation of arguments and uses a re‑entrant
      lock to guard against concurrent access.
    """
    # Basic argument validation
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(client_data, dict):
        return False

    with _cache_lock:
        # If client_id already exists, move it to the end (most recent)
        if client_id in _user_cache:
            _user_cache.move_to_end(client_id)

        # Insert or update the entry
        _user_cache[client_id] = client_data

        # Evict least‑recently used item if cache size exceeds the limit
        if len(_user_cache) > _MAX_CACHE_SIZE:
            # popitem(last=False) removes the first item (LRU)
            _user_cache.popitem(last=False)

    return True