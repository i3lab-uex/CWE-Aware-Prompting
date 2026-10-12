import threading
from typing import Dict, Any

# Global cache dictionary and a lock to guard concurrent access.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store user data in an in‑memory cache for fast retrieval.

    Args:
        user_id: A unique string identifier for the user.
        user_data: A dictionary containing user information.

    Returns:
        True if caching succeeded, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    # Use a lock to protect the shared cache from race conditions
    with _user_cache_lock:
        try:
            # Store a shallow copy to prevent external mutation
            user_cache[user_id] = dict(user_data)
        except Exception:
            # In case of any unexpected failure, do not raise
            return False

    return True