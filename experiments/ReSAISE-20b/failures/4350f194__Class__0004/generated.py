import collections
from typing import Dict

# Global cache with a maximum size to avoid uncontrolled memory growth (CWE-400)
_MAX_CACHE_SIZE = 10_000
user_cache: collections.OrderedDict[str, Dict] = collections.OrderedDict()


def cache_user_data(user_id: str, user_data: Dict) -> bool:
    """
    Store user data in an in-memory cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation: user_id must be a non-empty string
    if not isinstance(user_id, str) or not user_id:
        return False

    # Ensure the data is a dictionary
    if not isinstance(user_data, dict):
        return False

    # Enforce cache size limit to prevent uncontrolled resource consumption
    if len(user_cache) >= _MAX_CACHE_SIZE:
        # Remove the oldest item (FIFO)
        try:
            user_cache.popitem(last=False)
        except KeyError:
            # Cache was empty; nothing to evict
            pass

    # Insert or update the entry
    user_cache[user_id] = user_data
    return True

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    assert cache_user_data("user123", {"name": "Alice"}) is True
    print(user_cache)