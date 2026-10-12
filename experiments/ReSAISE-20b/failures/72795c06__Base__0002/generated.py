from collections import OrderedDict
import threading

# Global cache: an ordered dictionary to support LRU eviction.
user_cache = OrderedDict()

# Configuration
CACHE_MAX_SIZE = 1000          # Maximum number of entries in the cache.
_cache_lock = threading.Lock()  # Ensure thread‑safe access.

def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store or update a user's profile data in the in-memory cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for a user.
    profile_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    try:
        with _cache_lock:
            # If the key already exists, move it to the end (most recently used).
            if profile_id in user_cache:
                user_cache.move_to_end(profile_id)

            # Insert or update the entry.
            user_cache[profile_id] = profile_data

            # Evict least‑recently used entry if cache exceeds the maximum size.
            if len(user_cache) > CACHE_MAX_SIZE:
                # popitem(last=False) removes the oldest entry.
                user_cache.popitem(last=False)

        return True
    except Exception:
        # In a real application, you might log the exception here.
        return False