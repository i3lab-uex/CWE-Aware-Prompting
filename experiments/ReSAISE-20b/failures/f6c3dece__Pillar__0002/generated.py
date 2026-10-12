import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread‑safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic input validation
    if not isinstance(client_id, str):
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[client_id] = dict(client_data)
        return True
    except Exception:
        # Swallow any unexpected exception and signal failure
        return False