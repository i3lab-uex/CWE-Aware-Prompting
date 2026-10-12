import json
import threading

# Global cache dictionary and its lock for thread safety
user_cache: dict[str, dict] = {}
cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
MAX_CACHE_COUNT = 10_000          # maximum number of cached users
MAX_USER_DATA_BYTES = 1 << 20     # 1 MiB per user entry

def _data_size(data: dict) -> int:
    """
    Estimate the size in bytes of a user data dictionary by serializing it to JSON.
    This is a conservative estimate suitable for limiting memory usage.
    """
    try:
        return len(json.dumps(data).encode("utf-8"))
    except Exception:
        # Fallback: approximate with string conversion
        return len(str(data).encode("utf-8"))

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific information in the global `user_cache`.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was stored successfully, False otherwise.
    """
    # Basic input validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Enforce per-entry size limit
    if _data_size(data) > MAX_USER_DATA_BYTES:
        return False

    with cache_lock:
        # Enforce overall cache size limit
        if uid not in user_cache and len(user_cache) >= MAX_CACHE_COUNT:
            return False

        # Store a shallow copy to prevent external mutation
        user_cache[uid] = data.copy()

    return True