import sys
import threading

# Global cache dictionary and configuration limits
user_cache: dict[str, dict] = {}
CACHE_MAX_ENTRIES = 1000          # Maximum number of cached users
MAX_ENTRY_SIZE_BYTES = 1 << 20    # 1 MiB per user entry

# Thread‑safety lock
_cache_lock = threading.RLock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
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
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    # Prevent uncontrolled resource consumption by limiting size
    entry_size = sys.getsizeof(account_data)
    if entry_size > MAX_ENTRY_SIZE_BYTES:
        return False

    with _cache_lock:
        # If cache is full, evict the oldest entry (simple LRU)
        if len(user_cache) >= CACHE_MAX_ENTRIES:
            try:
                # Remove an arbitrary item (first key)
                oldest_key = next(iter(user_cache))
                del user_cache[oldest_key]
            except StopIteration:
                # Cache was empty; nothing to evict
                pass

        try:
            user_cache[account_id] = account_data.copy()
            return True
        except Exception:
            # Any unforeseen error results in a failure flag, no exception raised
            return False