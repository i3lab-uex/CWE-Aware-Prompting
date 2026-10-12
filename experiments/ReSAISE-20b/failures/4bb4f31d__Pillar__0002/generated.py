import threading
from typing import Dict, Any

# Global cache dictionary and a lock to guard concurrent access.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user-specific information in a global cache.

    Args:
        client_id: Unique identifier for the user.
        info_data: Dictionary containing user-related data.

    Returns:
        True if caching succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    try:
        # Ensure thread-safe update of the global cache
        with _user_cache_lock:
            user_cache[client_id] = info_data.copy()  # copy to avoid external mutation
        return True
    except Exception:
        # In case of unexpected errors, do not propagate exceptions.
        return False