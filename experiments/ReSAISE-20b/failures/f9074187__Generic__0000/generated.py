# -*- coding: utf-8 -*-

"""
Access control module.

Provides a single function `grant_access` that determines whether a user
is allowed to view a piece of content based on their role and subscription level.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Data structures – in a real application these would come from a database
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin",   "subscription_level": "vip"},
    2: {"role": "user",    "subscription_level": "free"},
    3: {"role": "user",    "subscription_level": "premium"},
    4: {"role": "user",    "subscription_level": "vip"},
}

CONTENT = {
    101: {"title": "Public Article",          "required_level": "free"},
    102: {"title": "Premium Video",           "required_level": "premium"},
    103: {"title": "VIP Exclusive Podcast",   "required_level": "vip"},
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

SUBSCRIPTION_ORDER = {
    "free": 0,
    "premium": 1,
    "vip": 2,
}

def _level_value(level: str) -> int:
    """
    Convert a subscription level string into an integer for comparison.
    Raises KeyError if the level is unknown.
    """
    return SUBSCRIPTION_ORDER[level]

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine whether a user can access the requested content.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    item_id : int
        Identifier of the content to access.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    TypeError
        If the arguments are not integers.
    KeyError
        If `user_id` or `item_id` is unknown.
    ValueError
        If the user role or subscription level is not recognized.
    """
    # Basic type checking – helps prevent accidental misuse
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be an integer; got {type(user_id).__name__}")
    if not isinstance(item_id, int):
        raise TypeError(f"item_id must be an integer; got {type(item_id).__name__}")

    # Retrieve user and content records
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"Unknown user ID: {user_id}") from exc

    try:
        content = CONTENT[item_id]
    except KeyError as exc:
        raise KeyError(f"Unknown content ID: {item_id}") from exc

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    if user_level is None:
        raise ValueError(f"User {user_id} has no subscription level defined.")
    if required_level is None:
        raise ValueError(f"Content {item_id} has no required level defined.")

    try:
        user_val = _level_value(user_level)
        req_val = _level_value(required_level)
    except KeyError as exc:
        raise ValueError(f"Unknown subscription level: {exc}") from exc

    if user_val >= req_val:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    for uid in USERS:
        for cid in CONTENT:
            print(f"User {uid} accessing content {cid}: {grant_access(uid, cid)}")