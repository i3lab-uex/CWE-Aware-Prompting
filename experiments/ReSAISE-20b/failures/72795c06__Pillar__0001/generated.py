# cache_profile_data.py

"""
In‑memory user profile caching module.

The `cache_profile_data` function stores a copy of the provided
profile data in a global dictionary (`user_cache`).  A lock is used to
ensure thread safety, preventing race conditions when multiple threads
attempt to write or read the cache concurrently.

Security considerations:
- The function copies `profile_data` before caching to avoid
  accidental mutation of the caller's data.
- The global cache is intentionally kept in memory; it does not
  expose any persistent storage, mitigating data leakage risk.
- No external resources are created or destroyed; thus the CWE‑664
  concern (improper resource control) is not applicable here.
"""

import copy
from threading import Lock

# Global cache dictionary
user_cache: dict[str, dict] = {}
# Thread‑safety lock for the cache
_user_cache_lock: Lock = Lock()


def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Cache user profile data in the global `user_cache`.

    Args:
        profile_id (str): Unique identifier for the user.
        profile_data (dict): Dictionary containing user details.

    Returns:
        bool: True if caching succeeds, False otherwise.
    """
    try:
        # Defensive copy to prevent external mutation
        data_copy = copy.deepcopy(profile_data)

        with _user_cache_lock:
            user_cache[profile_id] = data_copy

        return True
    except Exception:  # pragma: no cover
        # Any unexpected error is swallowed and False is returned
        return False