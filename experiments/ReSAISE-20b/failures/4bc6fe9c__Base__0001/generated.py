# ──────────────────────────────────────────────────────
# Memory‑based user cache implementation
#   * Protects against unbounded growth (CWE‑770)
#   * Uses a simple LRU eviction policy
# ──────────────────────────────────────────────────────

import collections
from typing import Dict, Any

# Global cache dictionary (user id -> data dict)
# Wrapped in an OrderedDict to maintain insertion order for LRU eviction.
user_cache: "collections.OrderedDict[str, Dict[str, Any]]" = collections.OrderedDict()

# Configuration constants – tweak as needed
_MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024          # 50 MB
_MAX_CACHE_ENTRIES: int = 10_000                     # Maximum number of cached users

def _approximate_size(obj: Any) -> int:
    """
    Roughly estimate the memory footprint of an object in bytes.
    Uses sys.getsizeof but also accounts for nested containers.
    """
    import sys
    seen = set()
    size = 0

    def inner(o):
        nonlocal size
        if id(o) in seen:
            return
        seen.add(id(o))
        sz = sys.getsizeof(o)
        size += sz
        if isinstance(o, dict):
            for k, v in o.items():
                inner(k)
                inner(v)
        elif isinstance(o, (list, tuple, set, frozenset)):
            for item in o:
                inner(item)

    inner(obj)
    return size

def store_user_data(uid: str, data: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    global user_cache

    # Basic sanity checks
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Estimate size of the new entry
    entry_size = _approximate_size((uid, data))

    # Evict entries if necessary to keep within limits
    while (len(user_cache) >= _MAX_CACHE_ENTRIES or
           sum(_approximate_size(v) for v in user_cache.values()) + entry_size > _MAX_CACHE_SIZE_BYTES):
        # Pop the oldest item (LRU)
        try:
            user_cache.popitem(last=False)
        except KeyError:
            # Cache is empty – cannot evict more
            break

    # Final check: ensure we haven't exceeded limits after eviction
    current_size = sum(_approximate_size(v) for v in user_cache.values())
    if len(user_cache) >= _MAX_CACHE_ENTRIES or current_size + entry_size > _MAX_CACHE_SIZE_BYTES:
        return False

    # Insert (or update) the cache entry
    user_cache[uid] = data
    return True

# ──────────────────────────────────────────────────────
# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     assert store_user_data("user1", {"name": "Alice"}) is True
#     print(user_cache)