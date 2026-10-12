import sys
from threading import RLock

# Global cache dictionary and its associated lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = RLock()

# Configuration limits to mitigate CWE‑770.
_MAX_CACHE_BYTES: int = 50 * 1024 * 1024   # 50 MB
_MAX_CACHE_ENTRIES: int = 10_000           # Maximum number of cached users


def _current_cache_size() -> int:
    """Return an approximate memory footprint of the cache in bytes."""
    total = 0
    for uid, data in user_cache.items():
        total += sys.getsizeof(uid) + sys.getsizeof(data)
    return total


def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user information in a memory‑based cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation: ensure inputs are of expected types
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    with _user_cache_lock:
        # Enforce maximum number of entries
        if uid not in user_cache and len(user_cache) >= _MAX_CACHE_ENTRIES:
            return False

        # Estimate the memory usage of this new entry
        entry_size = sys.getsizeof(uid) + sys.getsizeof(data)

        # Enforce maximum cache size
        if _current_cache_size() + entry_size > _MAX_CACHE_BYTES:
            return False

        # Store or update the cache
        user_cache[uid] = data.copy()  # shallow copy to avoid accidental mutations

    return True