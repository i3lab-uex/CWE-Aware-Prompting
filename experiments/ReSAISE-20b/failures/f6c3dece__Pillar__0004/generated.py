import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store the provided client data in the global user_cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client/user.
    client_data : dict
        Dictionary containing user-specific data to be cached.

    Returns
    -------
    bool
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Replace any existing entry for the client_id
            user_cache[client_id] = dict(client_data)  # shallow copy to avoid accidental mutation
        return True
    except Exception:
        # Swallow all exceptions and signal failure
        return False