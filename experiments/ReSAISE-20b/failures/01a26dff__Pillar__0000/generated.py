import threading
from typing import Dict

# Global cache and its lock for thread‑safety
user_cache: Dict[str, Dict] = {}
_user_cache_lock = threading.Lock()


def cache_account_info(account_id: str, account_data: Dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    account_id : str
        Unique identifier for the user.
    account_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic input validation to guard against misuse
    if not isinstance(account_id, str) or not account_id:
        return False

    if not isinstance(account_data, dict):
        return False

    try:
        # Use a lock to prevent race conditions in multi‑threaded environments
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # Do not expose internal errors; simply signal failure
        return False