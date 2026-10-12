import threading
from typing import Dict

# Global cache dictionary and a lock to ensure thread‑safe access.
user_cache: Dict[str, dict] = {}
_cache_lock = threading.RLock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store the supplied account data in the global `user_cache`.

    Args:
        account_id (str): Unique identifier for a user.
        account_data (dict): Dictionary of user details.

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # Do not propagate exceptions; simply indicate failure.
        return False