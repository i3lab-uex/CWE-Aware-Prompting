import threading
from typing import Dict, Any

# Global cache dictionary and a lock to protect concurrent access.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global `user_cache`.

    Args:
        identifier: A unique string that identifies each user.
        data_info: A dictionary containing various user-related information.

    Returns:
        True if the data was successfully cached, False otherwise.
    """
    # Basic type validation to avoid accidental corruption of the cache
    if not isinstance(identifier, str) or not isinstance(data_info, dict):
        return False

    # Acquire a re‑entrant lock to prevent race conditions and ensure
    # that the cache is not left in an inconsistent state.
    try:
        with _user_cache_lock:
            # Overwrite any existing entry for the same identifier.
            user_cache[identifier] = data_info.copy()
        return True
    except Exception:
        # In a real application you might log the exception here.
        return False