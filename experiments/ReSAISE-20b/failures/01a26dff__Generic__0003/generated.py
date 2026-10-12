from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: Dict[str, Any]) -> bool:
    """
    Store user-specific data in the global in-memory cache.

    Parameters
    ----------
    account_id : str
        A unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    try:
        # Basic validation: ensure account_id is a non-empty string
        if not isinstance(account_id, str) or not account_id.strip():
            return False

        # Ensure account_data is a dictionary
        if not isinstance(account_data, dict):
            return False

        # Store data in the cache atomically
        with _user_cache_lock:
            user_cache[account_id] = account_data.copy()

        return True
    except Exception:
        # Do not propagate exceptions; just signal failure
        return False