# cache_user_data.py

"""
A simple in‑memory user data caching module.

This implementation protects against CWE-770 (uncontrolled resource allocation)
by enforcing a maximum cache size. When the limit is reached, the least recently
used entry is evicted before adding a new one. The cache uses an OrderedDict to
track usage order.

Usage:
    from cache_user_data import cache_user_data, get_cached_user

    cache_user_data('user123', {'name': 'Alice', 'email': 'alice@example.com'})
    data = get_cached_user('user123')
"""

from collections import OrderedDict
import threading

# Global cache dictionary with thread‑safety
_user_cache_lock = threading.RLock()
_user_cache: OrderedDict[str, dict] = OrderedDict()

# Maximum number of entries to keep in cache
_CACHE_MAX_SIZE: int = 10_000

def _evict_if_needed() -> None:
    """
    Evicts the oldest entry if cache size exceeds _CACHE_MAX_SIZE.
    This function must be called while holding _user_cache_lock.
    """
    if len(_user_cache) > _CACHE_MAX_SIZE:
        # popitem(last=False) removes the first item (least recently used)
        _user_cache.popitem(last=False)

def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Store user data in the global cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation: ensure keys are strings and values are JSON‑serialisable
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    try:
        # Attempt to serialize to ensure data can be safely stored
        import json
        json.dumps(user_data)
    except (TypeError, OverflowError):
        return False

    with _user_cache_lock:
        # Move existing entry to end (most recently used)
        if user_id in _user_cache:
            _user_cache.pop(user_id)

        # Insert new entry
        _user_cache[user_id] = user_data

        # Evict old entries if cache is over the limit
        _evict_if_needed()

    return True

def get_cached_user(user_id: str) -> dict | None:
    """
    Retrieve cached user data, if present.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict | None
        The cached data or None if not found.
    """
    with _user_cache_lock:
        data = _user_cache.get(user_id)
        if data is not None:
            # Move accessed item to end to mark it as recently used
            _user_cache.move_to_end(user_id)
        return data

def clear_user_cache() -> None:
    """
    Clear the entire user cache. Useful for tests or maintenance.
    """
    with _user_cache_lock:
        _user_cache.clear()