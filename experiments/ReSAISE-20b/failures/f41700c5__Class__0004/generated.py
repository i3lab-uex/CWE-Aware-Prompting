import threading
from collections import OrderedDict

# Global cache with a maximum size to prevent uncontrolled resource consumption.
MAX_CACHE_SIZE = 10_000  # Adjust as needed for your environment
_user_cache_lock = threading.Lock()
user_cache: OrderedDict[str, dict] = OrderedDict()


def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in a memory‑based cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        Dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation: ensure identifier is a non‑empty string and data_info is a dict
    if not isinstance(identifier, str) or not identifier:
        return False

    if not isinstance(data_info, dict):
        return False

    with _user_cache_lock:
        # If the user is already cached, update the entry and move it to the end (most recent)
        if identifier in user_cache:
            user_cache.move_to_end(identifier)

        # Insert or update the entry
        user_cache[identifier] = data_info

        # Evict least‑recently used entries if we exceed the maximum size
        while len(user_cache) > MAX_CACHE_SIZE:
            # popitem(last=False) pops the oldest entry
            user_cache.popitem(last=False)

    return True