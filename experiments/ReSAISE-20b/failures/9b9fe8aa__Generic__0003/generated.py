import sys
import threading

# Global cache dictionary and bookkeeping structures
user_cache: dict[str, dict] = {}
_user_lock = threading.RLock()

# Configuration limits
_MAX_USERS: int = 1000          # maximum number of cached users
_MAX_CACHE_BYTES: int = 10 * 1024 * 1024  # 10 MiB

# Current cache statistics
_current_user_count: int = 0
_current_cache_size_bytes: int = 0


def _estimate_dict_size(d: dict) -> int:
    """
    Estimate the memory footprint of a dictionary in bytes.
    Uses sys.getsizeof recursively to approximate nested structures.
    """
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
        elif isinstance(o, (list, tuple, set)):
            for item in o:
                inner(item)

    inner(d)
    return size


def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store the provided `user_details` in the global `user_cache`
    under the key `user_identifier`.  The operation succeeds only
    if adding the new entry does not violate either the maximum
    user count or the total cache size limit.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing arbitrary user attributes.

    Returns
    -------
    bool
        True if the entry was cached, False otherwise.
    """
    global _current_user_count, _current_cache_size_bytes

    # Quick sanity checks
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(user_details, dict):
        return False

    # Estimate size of the new entry
    new_entry_size = _estimate_dict_size(user_details)

    with _user_lock:
        # If user already exists, remove its current size
        if user_identifier in user_cache:
            old_size = _estimate_dict_size(user_cache[user_identifier])
            _current_cache_size_bytes -= old_size
        else:
            # New user, increment count tentatively
            _current_user_count += 1

        # Check limits
        if (_current_user_count > _MAX_USERS or
                _current_cache_size_bytes + new_entry_size > _MAX_CACHE_BYTES):
            # Rollback count increment if it was a new user
            if user_identifier not in user_cache:
                _current_user_count -= 1
            else:
                # Restore old size if replacing existing user
                _current_cache_size_bytes += old_size
            return False

        # Update cache and statistics
        user_cache[user_identifier] = user_details.copy()
        _current_cache_size_bytes += new_entry_size

    return True