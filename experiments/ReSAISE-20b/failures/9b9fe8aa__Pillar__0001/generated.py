import sys
import threading
from copy import deepcopy

# Global cache dictionary and its lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits
_MAX_CACHE_ENTRIES: int = 10_000          # Maximum number of cached users
_MAX_TOTAL_SIZE_BYTES: int = 50 * 1024**2  # 50 MB total cache size

def _current_cache_size() -> int:
    """Return the current approximate memory usage of user_cache."""
    total = 0
    for value in user_cache.values():
        total += sys.getsizeof(value)
    return total

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store the given user details in the global cache.

    Parameters
    ----------
    user_identifier : str
        A unique string identifying the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully; False if adding it would exceed
        configured limits.

    Notes
    -----
    - The function uses a deep copy of user_details to avoid accidental mutation.
    - Thread‑safety is ensured via a global lock.
    """
    # Defensive checks
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    # Compute size of the new entry
    try:
        entry_size = sys.getsizeof(user_details)
    except Exception:
        return False

    with _user_cache_lock:
        # Enforce entry count limit
        if len(user_cache) >= _MAX_CACHE_ENTRIES:
            return False

        # Enforce total size limit
        current_size = _current_cache_size()
        if current_size + entry_size > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Store a defensive copy
        try:
            user_cache[user_identifier] = deepcopy(user_details)
        except Exception:
            return False

    return True