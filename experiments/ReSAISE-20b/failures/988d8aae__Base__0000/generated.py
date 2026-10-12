# cache_client_info.py

from typing import Dict, Any

# Global dictionary that holds cached user data.
# In a real application this might be replaced with a more sophisticated cache
# (e.g., Redis, memcached) or an LRU implementation.
user_cache: Dict[str, Dict[str, Any]] = {}

# Configuration constants for cache limits
MAX_CACHE_SIZE_BYTES = 50 * 1024 * 1024          # 50 MB total
MAX_CACHE_ENTRIES = 10_000                      # Maximum number of cached users

def _current_cache_size() -> int:
    """
    Estimate the current memory footprint of user_cache in bytes.
    Uses sys.getsizeof on keys and values. This is an approximation
    and may not reflect the true memory usage.
    """
    import sys
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size

def cache_client_info(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the client data was cached successfully.
        False if caching failed due to size or count constraints.
    """
    # Validate input types
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    # Enforce maximum entry count
    if len(user_cache) >= MAX_CACHE_ENTRIES:
        return False

    # Estimate new cache size if this entry were added
    import sys
    estimated_entry_size = (
        sys.getsizeof(client_id) + sys.getsizeof(client_data)
    )
    if _current_cache_size() + estimated_entry_size > MAX_CACHE_SIZE_BYTES:
        return False

    # Perform the caching operation
    try:
        user_cache[client_id] = client_data.copy()
    except Exception:
        # In case of any unexpected error, do not cache
        return False

    return True