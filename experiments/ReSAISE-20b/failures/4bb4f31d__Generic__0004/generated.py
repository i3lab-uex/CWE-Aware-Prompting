import threading
from typing import Dict

# Global cache dictionary
user_cache: Dict[str, dict] = {}
# Lock to make cache thread‑safe
_user_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user‑specific information in a global cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    info_data : dict
        Dictionary containing user data to be cached.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation: ensure types are correct
    if not isinstance(client_id, str) or not isinstance(info_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[client_id] = info_data.copy()
        return True
    except Exception:
        # Any unexpected exception is treated as a failure
        return False