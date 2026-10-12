#!/usr/bin/env python3
"""
A simple access control module that determines whether a user can view a piece of content.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures – in a real system these would come from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user",  "subscription_level": "basic"},
    3: {"role": "user",  "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial",   "required_level": "basic"},
    102: {"title": "Premium Workshop","required_level": "premium"},
    103: {"title": "Admin Guide",      "required_level": "admin"},
}

# --------------------------------------------------------------------------- #
# Subscription hierarchy – lower index = higher privilege
# --------------------------------------------------------------------------- #

SUBSCRIPTION_HIERARCHY = ["admin", "premium", "basic"]

def _subscription_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    If the level is unknown, treat it as lowest privilege (index 999).
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError:
        return 999

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine if a user is allowed to access a content item.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting access.
    item_id : int
        The ID of the content item.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    - Admin users have unrestricted access.
    - Regular users must meet or exceed the required subscription level of the content.
    """
    # Validate existence
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # Admins bypass checks
    if user.get("role") == "admin":
        return content["title"]

    # Compare subscription levels
    user_level = user.get("subscription_level", "")
    required_level = content.get("required_level", "")

    if _subscription_index(user_level) <= _subscription_index(required_level):
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tests = [
        (1, 101),  # admin accessing basic
        (2, 101),  # basic user accessing basic
        (2, 102),  # basic user accessing premium
        (3, 102),  # premium user accessing premium
        (4, 101),  # unknown user
    ]

    for uid, iid in tests:
        print(f"user {uid} accessing item {iid}: {grant_access(uid, iid)}")