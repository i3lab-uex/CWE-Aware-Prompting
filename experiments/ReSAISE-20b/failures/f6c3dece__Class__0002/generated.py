# In‑memory cache for user data with basic resource limits

from typing import Dict, Any

# Global cache dictionary
user_cache: Dict[str, Dict[str, Any]] = {}

# Configuration constants for resource limits
MAX_CACHE_ENTRIES: int = 10_000          # maximum number of cached users
MAX_ENTRY_SIZE_BYTES: int = 1_048_576     # maximum size (≈1 MB) per user data dict

def _dict_size_bytes(d: Dict[str, Any]) -> int:
    """
    Estimate the memory size of a dictionary in bytes.
    Uses sys.getsizeof recursively for values; may over‑estimate but is safe.
    """
    import sys
    size = sys.getsizeof(d)
    for v in d.values():
        size += sys.getsizeof(v)
    return size

def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Cache user data in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    # Enforce cache size limit
    if len(user_cache) >= MAX_CACHE_ENTRIES:
        # Optional: could evict least‑recently used entry here
        return False

    # Enforce per‑entry size limit to avoid uncontrolled memory consumption
    try:
        entry_size = _dict_size_bytes(client_data)
    except Exception:
        return False
    if entry_size > MAX_ENTRY_SIZE_BYTES:
        return False

    # Store in cache safely
    try:
        user_cache[client_id] = client_data.copy()
    except Exception:
        return False

    return True