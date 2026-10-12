import sys
import threading

# Global cache dictionary and related metadata
user_cache = {}
cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
MAX_ENTRIES = 10_000          # maximum number of cached users
MAX_TOTAL_SIZE_BYTES = 50 * 1024 * 1024  # ~50 MiB total cache size

# Track current total memory usage of cached values
_current_cache_size = 0


def _approximate_dict_size(d: dict) -> int:
    """
    Roughly estimate the memory footprint of a dictionary in bytes.
    This is an approximation; for more accurate measurements,
    consider using the `pympler` library or similar tools.
    """
    size = sys.getsizeof(d)
    for key, value in d.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Cache user information in the global `user_cache` dictionary.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    global _current_cache_size

    # Basic validation
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    # Estimate size of the new entry
    entry_size = _approximate_dict_size(client_data)

    with cache_lock:
        # If the key already exists, adjust size difference
        existing = user_cache.get(client_id)
        if existing is not None:
            old_size = _approximate_dict_size(existing)
            size_delta = entry_size - old_size
        else:
            # New key: check overall limits first
            if len(user_cache) >= MAX_ENTRIES:
                return False
            size_delta = entry_size

        # Check total size constraint
        if _current_cache_size + size_delta > MAX_TOTAL_SIZE_BYTES:
            return False

        # Perform the cache update
        user_cache[client_id] = client_data
        _current_cache_size += size_delta

    return True