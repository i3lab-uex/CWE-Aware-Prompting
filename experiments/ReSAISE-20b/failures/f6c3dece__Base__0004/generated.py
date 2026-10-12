import threading
from typing import Dict

# Global cache dictionary and a lock for thread‑safe access
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Maximum number of entries allowed in the cache (CWE‑770 mitigation)
_MAX_CACHE_SIZE = 10_000

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    client_data : dict
        Dictionary containing details about the user.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid malicious or malformed inputs
    if not isinstance(client_id, str) or not client_id:
        return False

    # Ensure the data is serializable and shallow‑copyable
    try:
        cached_data = dict(client_data)
    except Exception:
        return False

    with _user_cache_lock:
        # Enforce cache size limit
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Remove an arbitrary entry (e.g., the first one) to free space
            try:
                user_cache.pop(next(iter(user_cache)))
            except StopIteration:
                # Cache is unexpectedly empty; treat as failure
                return False

        try:
            user_cache[client_id] = cached_data
            return True
        except Exception:
            # Any unforeseen error (e.g., memory exhaustion) results in failure
            return False