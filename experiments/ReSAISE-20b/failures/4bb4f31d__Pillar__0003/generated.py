import threading
import copy

# Global cache dictionary and a lock to guard concurrent access
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user-specific information in a global cache.

    Args:
        client_id: Unique identifier for the user.
        info_data: Dictionary containing user-related data.

    Returns:
        bool: True if the data was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    try:
        # Use a deep copy to prevent external mutation of cached data
        with _cache_lock:
            user_cache[client_id] = copy.deepcopy(info_data)
    except Exception:
        # Any unexpected error should not propagate
        return False

    return True