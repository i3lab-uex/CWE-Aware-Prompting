import json
import sys
from threading import RLock

# Global cache dictionary: client_id -> client_data
user_cache = {}
# Thread‑safety lock for concurrent access
_cache_lock = RLock()

# Configuration limits (adjust as needed)
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024   # 10 MiB
_MAX_CLIENTS = 1000


def _current_cache_size() -> int:
    """Return the current size of the cache in bytes."""
    total = 0
    for data in user_cache.values():
        # Rough estimate: size of the JSON representation
        try:
            total += len(json.dumps(data).encode('utf-8'))
        except Exception:
            # Fallback to sys.getsizeof if serialization fails
            total += sys.getsizeof(data)
    return total


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific details in a global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully,
        False if adding it would exceed size or count limits.
    """
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    with _cache_lock:
        # If the client already exists, replace it directly
        if client_id in user_cache:
            user_cache[client_id] = client_data
            return True

        # Enforce maximum number of clients
        if len(user_cache) >= _MAX_CLIENTS:
            return False

        # Estimate new size
        try:
            entry_size = len(json.dumps(client_data).encode('utf-8'))
        except Exception:
            entry_size = sys.getsizeof(client_data)

        if _current_cache_size() + entry_size > _MAX_CACHE_SIZE_BYTES:
            return False

        user_cache[client_id] = client_data
        return True