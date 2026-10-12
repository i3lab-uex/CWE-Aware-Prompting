import json
import threading

# Global cache and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits to mitigate CWE‑400
_MAX_CACHE_ENTRIES: int = 10_000            # maximum number of cached users
_MAX_ENTRY_SIZE_BYTES: int = 1_048_576      # maximum size of a single user dict (~1 MB)

def _entry_size_bytes(data_info: dict) -> int:
    """
    Estimate the byte size of a user data dictionary by serializing it to JSON.
    This is a simple heuristic; for more accurate measurement, consider
    using sys.getsizeof or a custom serializer.
    """
    try:
        return len(json.dumps(data_info).encode("utf-8"))
    except (TypeError, ValueError):
        # If the dict contains non‑serializable objects, treat as too large
        return _MAX_ENTRY_SIZE_BYTES + 1

def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    identifier : str
        Unique string identifying a user.
    data_info : dict
        Dictionary containing arbitrary user‑related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type checks (no exceptions raised)
    if not isinstance(identifier, str) or not isinstance(data_info, dict):
        return False

    # Enforce size limits
    if _entry_size_bytes(data_info) > _MAX_ENTRY_SIZE_BYTES:
        return False

    with _user_cache_lock:
        # Prevent cache from growing beyond the configured maximum
        if len(user_cache) >= _MAX_CACHE_ENTRIES and identifier not in user_cache:
            return False

        # Store or update the entry
        user_cache[identifier] = data_info.copy()  # shallow copy to avoid accidental mutation

    return True