import threading

# Global cache dictionary and a lock for thread safety
user_cache: dict[str, dict] = {}
_CACHE_LOCK = threading.RLock()
_MAX_CACHE_SIZE = 10_000          # Maximum number of cached users
_MIN_DATA_SIZE_BYTES = 1024       # Minimum size (bytes) for data_info to be cached

def _data_size_bytes(data: dict) -> int:
    """
    Estimate the memory size of `data` in bytes.
    This is a rough approximation using the length of its string representation.
    """
    try:
        return len(str(data).encode("utf-8"))
    except Exception:
        # Fallback if encoding fails
        return 0

def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in a global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        A dictionary containing various user-related information.

    Returns
    -------
    bool
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(data_info, dict):
        return False

    # Prevent uncontrolled resource consumption:
    # 1. Enforce a maximum cache size
    # 2. Reject data that is too large
    if _data_size_bytes(data_info) < _MIN_DATA_SIZE_BYTES:
        # Data too small to be worth caching
        return False

    with _CACHE_LOCK:
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Cache is full; reject new entries to avoid uncontrolled growth
            return False

        try:
            # Store a shallow copy to prevent external mutation
            user_cache[identifier] = data_info.copy()
        except Exception:
            # Any unforeseen error results in a failed cache operation
            return False

    return True