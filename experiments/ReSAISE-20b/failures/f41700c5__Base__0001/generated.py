# -*- coding: utf-8 -*-

"""
Memory‑based caching system for user data.

The cache is implemented as a simple dictionary that maps unique
identifiers to the corresponding user information dictionaries.
To mitigate CWE‑770 (unbounded resource allocation), a maximum cache
size is enforced. When the limit is reached, new entries are rejected.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread‑safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_CACHE_LOCK = threading.RLock()

# Maximum number of entries allowed in the cache. Adjust as needed.
_MAX_CACHE_SIZE = 10_000


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        Dictionary containing various user‑related information.

    Returns
    -------
    bool
        ``True`` if the entry was stored successfully, ``False`` if the cache
        has reached its maximum size and the new entry is rejected.

    Notes
    -----
    * The function uses a re‑entrant lock to ensure thread safety.
    * If the cache size exceeds :data:`_MAX_CACHE_SIZE`, the new entry
      is not added to prevent uncontrolled memory growth.
    """
    if not isinstance(identifier, str):
        raise TypeError("identifier must be a string")

    if not isinstance(data_info, dict):
        raise TypeError("data_info must be a dictionary")

    with _CACHE_LOCK:
        if len(user_cache) >= _MAX_CACHE_SIZE and identifier not in user_cache:
            # Cache is full and we are trying to add a new key
            return False

        # Store or update the entry
        user_cache[identifier] = data_info.copy()  # copy to avoid accidental mutation

    return True