import threading
from typing import Dict

# Global cache dictionary and a lock for thread‑safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store or update user‑specific information in the global cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for a user.
    info_data : dict
        User related information to be cached.

    Returns
    -------
    bool
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store or overwrite the entry
            user_cache[client_id] = info_data.copy()
        return True
    except Exception:
        # Unexpected failure – do not raise, just indicate failure
        return False