import sys
import threading
from typing import Dict

# Global cache and configuration parameters
user_cache: Dict[str, dict] = {}
_CACHE_LOCK = threading.RLock()

# Maximum allowed entries in the cache
_MAX_ENTRIES: int = 1000

# Approximate maximum size (in bytes) the cache can hold
_MAX_CACHE_SIZE: int = 10 * 1024 * 1024  # 10 MB

# Current size of the cache (approximate)
_current_cache_size: int = 0


def _estimate_dict_size(d: dict) -> int:
    """
    Estimate the memory footprint of a dictionary.
    This is an approximation using sys.getsizeof on the dict and its items.
    """
    size = sys.getsizeof(d)
    for key, value in d.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size


def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user-specific details in a global cache.

    Parameters
    ----------
    user_identifier : str
        A unique string identifier assigned to each user.
    user_details : dict
        A dictionary containing various attributes and details related to the user.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (e.g., size or count limits exceeded).
    """
    global _current_cache_size

    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    # Estimate size of the new entry
    entry_size = _estimate_dict_size(user_details)

    with _CACHE_LOCK:
        # Check for size constraints
        if len(user_cache) >= _MAX_ENTRIES and user_identifier not in user_cache:
            # Cache is full; reject new entries
            return False

        if _current_cache_size + entry_size > _MAX_CACHE_SIZE and user_identifier not in user_cache:
            # Cache would exceed size limit; reject new entries
            return False

        # If updating an existing entry, adjust the size difference
        if user_identifier in user_cache:
            old_size = _estimate_dict_size(user_cache[user_identifier])
            _current_cache_size -= old_size

        # Store the new entry
        user_cache[user_identifier] = user_details.copy()
        _current_cache_size += entry_size

    return True