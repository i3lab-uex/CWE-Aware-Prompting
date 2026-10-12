import sys
import threading

# Global cache dictionary and its lock for thread safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Configuration limits
_MAX_ENTRIES = 10_000          # Maximum number of cached users
_MAX_TOTAL_BYTES = 10 * 1024 * 1024  # Maximum total memory usage (≈10 MiB)

# Current metrics
_current_entry_count = 0
_current_total_bytes = 0


def _current_cache_size() -> int:
    """Return the current total size in bytes of all cached values."""
    return _current_total_bytes


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store or update a client's data in the global user_cache.

    The function enforces limits on the number of cached entries and the
    total memory consumption.  It uses a lock to ensure thread safety.

    Parameters:
        client_id (str): Unique identifier for the user.
        client_data (dict): Dictionary containing the user's data.

    Returns:
        bool: True if the cache operation succeeded, False otherwise.
    """
    global _current_entry_count, _current_total_bytes

    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    data_size = sys.getsizeof(client_id) + sys.getsizeof(client_data)

    with _cache_lock:
        # If the client already exists, adjust current size accordingly
        if client_id in user_cache:
            old_size = sys.getsizeof(client_id) + sys.getsizeof(user_cache[client_id])
            _current_total_bytes -= old_size
        else:
            # New entry: check limits
            if _current_entry_count >= _MAX_ENTRIES:
                return False

        # Check total memory limit
        if (_current_total_bytes + data_size) > _MAX_TOTAL_BYTES:
            return False

        # Store/update the entry
        user_cache[client_id] = client_data
        _current_total_bytes += data_size

        if client_id not in user_cache:
            _current_entry_count += 1

    return True