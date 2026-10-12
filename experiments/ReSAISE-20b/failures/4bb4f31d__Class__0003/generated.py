import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to prevent uncontrolled growth
_MAX_CACHE_ENTRIES = 10_000


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Stores user-specific information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    info_data : dict
        Dictionary containing user-related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid storing malformed entries
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    with _user_cache_lock:
        # Enforce maximum cache size to avoid uncontrolled memory consumption
        if len(user_cache) >= _MAX_CACHE_ENTRIES:
            # Simple eviction strategy: remove the oldest entry
            try:
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]
            except StopIteration:
                # Cache was empty; nothing to evict
                pass

        try:
            user_cache[client_id] = info_data.copy()  # store a shallow copy
        except Exception:
            # In case of unforeseen errors (e.g., memory error), fail gracefully
            return False

    return True