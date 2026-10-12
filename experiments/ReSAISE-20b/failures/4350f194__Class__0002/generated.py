# cache_user_data.py

import threading
from typing import Dict, Any

# Global cache dictionary and lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()

# Maximum number of users to keep in cache (adjust as needed)
_MAX_CACHE_SIZE = 10_000

# Optional maximum size of a single user data dictionary (bytes)
_MAX_USER_DATA_SIZE = 1_048_576  # 1 MB


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Cache user data in memory for quick access.

    Args:
        user_id (str): A unique identifier for the user.
        user_data (dict): A dictionary containing user information.

    Returns:
        bool: True if caching was successful, False otherwise.
    """
    # Basic input validation
    if not isinstance(user_id, str) or not user_id:
        return False

    if not isinstance(user_data, dict):
        return False

    # Optional: limit the size of user_data to prevent excessive memory usage
    try:
        import sys
        data_size = sys.getsizeof(user_data)
        if data_size > _MAX_USER_DATA_SIZE:
            return False
    except Exception:
        # If size calculation fails, fallback to caching but log warning if needed
        pass

    with _user_cache_lock:
        # Enforce cache size limit (CWE-400 mitigation)
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Evict an arbitrary entry (FIFO/LRU policy can be implemented if needed)
            try:
                evicted_key = next(iter(user_cache))
                del user_cache[evicted_key]
            except StopIteration:
                pass  # Cache was empty, unlikely but safe

        user_cache[user_id] = user_data
    return True