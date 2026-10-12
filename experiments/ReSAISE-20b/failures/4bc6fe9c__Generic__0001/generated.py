import json
import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}
# Lock for thread‑safe operations on the cache
_cache_lock = threading.Lock()

# Configuration limits
_MAX_USER_COUNT: int = 10_000          # maximum number of cached users
_MAX_USER_SIZE_BYTES: int = 1 * 1024 * 1024  # 1 MiB per user

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for a user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Check size of the data by serialising to JSON
    try:
        serialized = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    except (TypeError, OverflowError):
        return False
    if len(serialized.encode('utf-8')) > _MAX_USER_SIZE_BYTES:
        return False

    with _cache_lock:
        # Enforce total count limit
        if uid not in user_cache and len(user_cache) >= _MAX_USER_COUNT:
            return False
        # Store or update the entry
        user_cache[uid] = data

    return True