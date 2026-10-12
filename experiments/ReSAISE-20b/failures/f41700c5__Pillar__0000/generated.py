import threading
from typing import Dict, Any

# Global cache for user data. Use a thread‑safe approach.
_user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.RLock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        Dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation: identifier must be a non‑empty string
    if not isinstance(identifier, str) or not identifier.strip():
        return False

    # Ensure data_info is a dictionary
    if not isinstance(data_info, dict):
        return False

    # Store data atomically to avoid race conditions
    with _cache_lock:
        # Avoid accidental overwrites if identifier already exists
        if identifier in _user_cache:
            return False  # or update with: _user_cache[identifier] = data_info

        try:
            # Copy the dictionary to prevent external mutation after caching
            _user_cache[identifier] = dict(data_info)
        except Exception:
            return False

    return True