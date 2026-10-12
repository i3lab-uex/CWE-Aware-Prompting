# Memory‑based user information cache implementation

import sys
from collections import OrderedDict
from typing import Dict, Any

# Global cache dictionary (OrderedDict preserves insertion order for potential eviction)
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

# Configuration limits
MAX_CACHE_ENTRIES: int = 10_000          # maximum number of cached users
MAX_TOTAL_SIZE_BYTES: int = 50 * 1024 * 1024  # ~50 MB total cache size

def _current_cache_size() -> int:
    """Return the current approximate memory usage of the cache in bytes."""
    size = 0
    for user_id, details in user_cache.items():
        size += sys.getsizeof(user_id)
        size += sys.getsizeof(details)
        # Rough estimate for nested dict items
        for key, value in details.items():
            size += sys.getsizeof(key)
            size += sys.getsizeof(value)
    return size

def cache_user_info(user_identifier: str, user_details: Dict[str, Any]) -> bool:
    """
    Store or update a user's details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    global user_cache

    # Basic validation
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    # If the user is already cached, update entry (no size check needed)
    if user_identifier in user_cache:
        user_cache[user_identifier] = user_details
        return True

    # Check entry count limit
    if len(user_cache) >= MAX_CACHE_ENTRIES:
        return False

    # Estimate new entry size
    entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)
    for k, v in user_details.items():
        entry_size += sys.getsizeof(k) + sys.getsizeof(v)

    # Check total size limit
    if _current_cache_size() + entry_size > MAX_TOTAL_SIZE_BYTES:
        return False

    # Insert new entry
    user_cache[user_identifier] = user_details
    return True