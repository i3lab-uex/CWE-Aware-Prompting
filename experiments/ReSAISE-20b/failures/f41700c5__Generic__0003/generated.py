# Memory‑based user cache implementation

from __future__ import annotations
import threading
from typing import Dict, Any

# Global cache dictionary and lock for thread‑safety
user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user information in the global `user_cache`.

    Parameters
    ----------
    identifier : str
        Unique user identifier.
    data_info : dict
        Dictionary containing user‑specific information.

    Returns
    -------
    bool
        True if the data was stored successfully, False otherwise.
    """
    # Basic type validation to avoid corrupting the cache
    if not isinstance(identifier, str):
        return False

    if not isinstance(data_info, dict):
        return False

    # Prevent storing empty identifiers or data
    if not identifier.strip() or not data_info:
        return False

    try:
        with _cache_lock:
            # Deep copy to avoid accidental external mutation
            user_cache[identifier] = dict(data_info)
        return True
    except Exception:
        # In practice, log the exception. Here we simply return False.
        return False