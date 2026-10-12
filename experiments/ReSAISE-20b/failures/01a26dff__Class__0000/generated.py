import threading
from collections import OrderedDict

# Global cache with a maximum capacity and size limit per entry.
_MAX_CACHE_SIZE = 1000               # Maximum number of cached accounts
_MAX_ENTRY_BYTES = 1 * 1024 * 1024   # Maximum size of account_data in bytes (~1 MB)

# Thread‑safe ordered dictionary to maintain insertion order for eviction.
_user_cache = OrderedDict()
_cache_lock = threading.Lock()


def _size_of_dict(d: dict) -> int:
    """
    Estimate the memory size of a dictionary in bytes.
    This is a heuristic using repr length; for more accurate measurement,
    the `sys.getsizeof` could be used, but that only measures the dict object
    itself and not its contents.
    """
    try:
        return len(repr(d).encode('utf-8'))
    except Exception:
        # Fallback if repr fails
        return 0


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in an in-memory cache.

    Parameters
    ----------
    account_id : str
        A unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    # Enforce size limits to mitigate uncontrolled resource consumption
    entry_size = _size_of_dict(account_data)
    if entry_size > _MAX_ENTRY_BYTES:
        return False

    with _cache_lock:
        # Evict oldest entry if cache is full
        if account_id not in _user_cache and len(_user_cache) >= _MAX_CACHE_SIZE:
            # Remove the first item (FIFO eviction)
            _user_cache.popitem(last=False)

        # Store or update the entry
        _user_cache[account_id] = account_data

    return True


# Optional helper to retrieve cached data (not part of the task but useful for testing)
def get_cached_account_info(account_id: str):
    with _cache_lock:
        return _user_cache.get(account_id)