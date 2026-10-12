import threading
from typing import Dict

# Global cache dictionary and a lock for thread‑safety
user_cache: Dict[str, Dict] = {}
_cache_lock = threading.Lock()


def cache_client_data(client_id: str, client_data: Dict) -> bool:
    """
    Store the provided `client_data` in the global `user_cache` under the key
    `client_id`. The operation is thread‑safe and returns True on success.
    
    Parameters
    ----------
    client_id : str
        A unique identifier for the user. Must be a non‑empty string.
    client_data : dict
        A dictionary containing arbitrary user data. Must be a mapping.
    
    Returns
    -------
    bool
        True if the cache entry was added/updated successfully, False otherwise.
    
    Notes
    -----
    - The function performs basic type validation to avoid corrupting the cache.
    - It uses a global lock to ensure that concurrent writes do not race.
    """
    # Basic input validation
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(client_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[client_id] = client_data.copy()
        return True
    except Exception:
        # In the unlikely event of an exception, we swallow it and return False
        return False