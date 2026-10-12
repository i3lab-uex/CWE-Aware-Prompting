import threading
from collections import OrderedDict

# Global cache with a maximum size to prevent uncontrolled resource consumption.
_MAX_CACHE_SIZE = 1000
_user_cache: "OrderedDict[str, dict]" = OrderedDict()
_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for each user.
    info_data : dict
        User-related data to cache.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    with _lock:
        # If the key already exists, move it to the end (most recent).
        if client_id in _user_cache:
            del _user_cache[client_id]

        # Add the new entry.
        _user_cache[client_id] = info_data

        # Enforce cache size limit.
        if len(_user_cache) > _MAX_CACHE_SIZE:
            # Pop the oldest item (first inserted).
            _user_cache.popitem(last=False)

    return True