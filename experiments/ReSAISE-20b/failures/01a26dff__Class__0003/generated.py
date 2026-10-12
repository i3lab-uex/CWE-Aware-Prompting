# In‑memory user account cache with size control and thread safety

from collections import OrderedDict
import threading
from typing import Dict, Any

# Global cache and configuration
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
_cache_lock = threading.RLock()          # Re‑entrant lock for thread safety
_MAX_CACHE_SIZE: int = 1000              # Maximum number of cached entries


def cache_account_info(account_id: str, account_data: Dict[str, Any]) -> bool:
    """
    Store user-specific data in the global `user_cache`.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(account_id, str) or not account_id:
        return False

    if not isinstance(account_data, dict):
        return False

    with _cache_lock:
        # Evict the oldest entry if cache size limit is reached
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Pop the first item (least recently added)
            user_cache.popitem(last=False)

        # Insert or update the entry
        try:
            user_cache[account_id] = account_data
            # Move to the end to mark as most recently used (optional)
            user_cache.move_to_end(account_id, last=True)
        except Exception:
            # Any exception during cache update is considered a failure
            return False

    return True