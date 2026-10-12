import sys
from typing import Dict

# Global cache dictionary and associated limits
user_cache: Dict[str, dict] = {}
_MAX_ENTRIES = 1000          # Maximum number of cached users
_MAX_TOTAL_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB total cache size

# Internal counter to keep track of current total size
_current_total_size_bytes = 0


def _size_of_dict(d: dict) -> int:
    """
    Estimate the memory footprint of a dictionary object.
    Uses sys.getsizeof recursively on keys and values.
    """
    size = sys.getsizeof(d)
    for k, v in d.items():
        size += sys.getsizeof(k) + sys.getsizeof(v)
    return size


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    global _current_total_size_bytes

    # Validate inputs
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    # Calculate the size of the new entry
    new_entry_size = _size_of_dict(client_data)

    # Check for count limit
    if client_id not in user_cache and len(user_cache) >= _MAX_ENTRIES:
        return False

    # Check for size limit
    projected_total = _current_total_size_bytes - (
        _size_of_dict(user_cache[client_id]) if client_id in user_cache else 0
    ) + new_entry_size

    if projected_total > _MAX_TOTAL_SIZE_BYTES:
        return False

    # Update cache and size counter
    if client_id in user_cache:
        _current_total_size_bytes -= _size_of_dict(user_cache[client_id])
    user_cache[client_id] = client_data
    _current_total_size_bytes += new_entry_size

    return True