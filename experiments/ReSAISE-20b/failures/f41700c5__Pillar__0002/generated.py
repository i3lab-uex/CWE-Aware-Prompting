import threading
from typing import Dict, Any

# Global cache dictionary and a lock to guard concurrent access
user_cache: Dict[str, Dict[str, Any]] = {}
cache_lock = threading.Lock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global cache.

    Args:
        identifier (str): A unique string that identifies each user.
        data_info (dict): A dictionary containing user-related information.

    Returns:
        bool: True if caching succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(data_info, dict):
        return False

    # Ensure the data is serializable and size-limited to mitigate memory abuse
    try:
        import json
        # Attempt to serialize; this will catch unserializable objects
        json.dumps(data_info)
    except (TypeError, OverflowError):
        return False

    # Enforce a reasonable size limit (e.g., 1 MB per entry)
    if len(json.dumps(data_info).encode('utf-8')) > 1 * 1024 * 1024:
        return False

    # Use a lock to prevent race conditions and ensure resource control
    try:
        with cache_lock:
            user_cache[identifier] = data_info.copy()
        return True
    except Exception:
        # Any unexpected error should not crash the application
        return False