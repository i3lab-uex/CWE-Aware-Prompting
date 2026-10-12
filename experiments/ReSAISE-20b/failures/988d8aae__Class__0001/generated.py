import sys
import threading

# Global cache dictionary and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()

# Configuration limits (adjust as needed)
_MAX_CACHE_COUNT = 10_000                # maximum number of cached entries
_MAX_TOTAL_SIZE_BYTES = 50 * 1024 * 1024 # ~50 MiB total size of cached data

def _current_cache_size() -> int:
    """Return the current approximate memory size of all cached client data."""
    return sum(sys.getsizeof(v) for v in user_cache.values())

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store the provided `client_data` in the global cache under `client_id`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid caching obviously invalid entries
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    # Estimate the size of the new entry
    new_entry_size = sys.getsizeof(client_data)

    with _cache_lock:
        # Enforce cache size and count limits
        if len(user_cache) >= _MAX_CACHE_COUNT:
            # Optionally evict the oldest entry (simple FIFO eviction)
            oldest_key = next(iter(user_cache))
            del user_cache[oldest_key]

        # If adding the new entry would exceed total size, reject it
        if _current_cache_size() + new_entry_size > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Store or update the entry
        user_cache[client_id] = client_data
        return True