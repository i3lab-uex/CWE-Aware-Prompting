#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Memory‑based cache for user/client information.

The module defines a global dictionary `user_cache` that stores
client data keyed by the unique client identifier.  The cache
enforces two limits:

* `MAX_CACHE_SIZE` – the maximum number of entries that can be stored.
* `MAX_ENTRY_SIZE_BYTES` – an upper bound on the size of a single
  entry (in bytes) to guard against unexpectedly large payloads.

The function :func:`cache_client_info` performs the insertion while
respecting these limits.  It returns ``True`` on success and
``False`` if the operation would violate any constraint.

The implementation is deliberately simple but thread‑safe: a
``threading.Lock`` protects all modifications to the cache.
"""

from __future__ import annotations

import json
import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global cache and configuration
# --------------------------------------------------------------------------- #

#: Central storage for cached user information.
user_cache: Dict[str, Dict[str, Any]] = {}

#: Maximum number of entries the cache can hold.
MAX_CACHE_SIZE: int = 10_000

#: Maximum allowed size of a single cache entry (in bytes).
# This helps prevent a client from flooding the cache with huge payloads.
MAX_ENTRY_SIZE_BYTES: int = 1_048_576  # 1 MiB

#: Lock to ensure thread‑safe access to the cache.
_cache_lock = threading.Lock()


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _entry_size_bytes(entry: Dict[str, Any]) -> int:
    """
    Estimate the size of a cache entry in bytes.

    The function serialises the dictionary to JSON and returns the length
    of the resulting byte string.  This is a conservative estimate that
    includes keys, values and structural overhead.

    Args:
        entry: The dictionary representing the client data.

    Returns:
        int: Size of the entry in bytes.
    """
    try:
        json_bytes = json.dumps(entry, separators=(",", ":")).encode("utf-8")
    except (TypeError, OverflowError):
        # Fallback: approximate size using Python's object repr
        json_bytes = str(entry).encode("utf-8")
    return len(json_bytes)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def cache_client_info(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store a client's information in the global cache.

    The function first checks that adding this entry will not exceed
    either the maximum number of entries or the per‑entry size limit.
    If both checks pass, the entry is inserted (or updated) in the
    cache.

    No exceptions are raised; failures are indicated by a ``False`` return value.

    Args:
        client_id: A unique string identifier for the user.
        client_data: Dictionary containing user attributes.

    Returns:
        bool: ``True`` if the entry was cached successfully,
              ``False`` otherwise.
    """
    # Quick sanity checks
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(client_data, dict):
        return False

    entry_size = _entry_size_bytes(client_data)
    if entry_size > MAX_ENTRY_SIZE_BYTES:
        # Entry too large; reject to avoid uncontrolled resource consumption.
        return False

    with _cache_lock:
        # If the client is already cached, we allow replacement without
        # affecting the total count.  This prevents accidental growth.
        if client_id not in user_cache and len(user_cache) >= MAX_CACHE_SIZE:
            # Cache full; cannot add new entry.
            return False

        user_cache[client_id] = client_data
    return True


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Populate cache with a sample entry
    result = cache_client_info("user123", {"name": "Alice", "age": 30})
    print(f"Cached: {result}")   # Expected: True

    # Attempt to cache a very large entry
    huge_data = {"data": "x" * (MAX_ENTRY_SIZE_BYTES + 1)}
    result = cache_client_info("user_large", huge_data)
    print(f"Cached large entry: {result}")  # Expected: False