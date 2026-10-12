import sys
import threading
from typing import Dict

# Global cache and associated lock for thread‑safety
user_cache: Dict[str, dict] = {}
cache_lock = threading.Lock()

# Configuration limits to mitigate CWE‑770
MAX_CACHE_COUNT: int = 10_000          # maximum number of cached users
MAX_TOTAL_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB total size

def _current_cache_size() -> int:
    """
    Compute the approximate memory footprint of all cached values.
    This is a heuristic and may over‑estimate due to Python's memory allocator.
    """
    total = 0
    for data in user_cache.values():
        total += sys.getsizeof(data)
    return total

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user information in the global cache if limits allow.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (size or count limit exceeded).
    """
    # Basic validation
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    with cache_lock:
        # Enforce maximum number of entries
        if len(user_cache) >= MAX_CACHE_COUNT and client_id not in user_cache:
            return False

        # Estimate size impact of adding this entry
        new_entry_size = sys.getsizeof(client_data)
        current_total = _current_cache_size()
        if client_id not in user_cache:
            # New entry, check against total size limit
            if current_total + new_entry_size > MAX_TOTAL_SIZE_BYTES:
                return False

        # Cache the data (replace if already present)
        user_cache[client_id] = client_data
    return True