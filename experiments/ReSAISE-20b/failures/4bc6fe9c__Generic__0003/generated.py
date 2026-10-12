import sys
from typing import Dict

# Global cache dictionary
user_cache: Dict[str, dict] = {}

# Cache limits
_MAX_ITEMS = 1000          # maximum number of cached users
_MAX_SIZE_BYTES = 5 * 1024 * 1024  # maximum total size (~5 MB)

def _current_cache_size() -> int:
    """Return the current approximate memory usage of user_cache."""
    size = 0
    for uid, data in user_cache.items():
        size += sys.getsizeof(uid)
        size += sys.getsizeof(data)
    return size

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific data in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for a user.
    data : dict
        Dictionary of user attributes.

    Returns
    -------
    bool
        True if data was cached successfully, False otherwise.
    """
    # Basic type validation (optional but helps catch misuse)
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    # Check item count limit
    if len(user_cache) >= _MAX_ITEMS and uid not in user_cache:
        return False

    # Estimate size increase
    additional_size = sys.getsizeof(uid) + sys.getsizeof(data)
    current_size = _current_cache_size()
    if current_size + additional_size > _MAX_SIZE_BYTES and uid not in user_cache:
        return False

    # Store or update the cache entry
    user_cache[uid] = data
    return True