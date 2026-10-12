# -*- coding: utf-8 -*-
"""
Content access control module.

This module defines a single function `grant_access` that determines whether
a user is allowed to view a piece of content based on their role and
subscription level.  The implementation follows best practices for
access‑control logic and guards against common weaknesses such as
CWE-284 (Improper Access Control).
"""

from __future__ import annotations

from typing import Dict, Final


# --------------------------------------------------------------------------- #
# Example data structures
# --------------------------------------------------------------------------- #

USERS: Final[Dict[int, Dict[str, str]]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Final[Dict[int, Dict[str, str]]] = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Premium Workshop", "required_level": "premium"},
    103: {"title": "Admin Guide", "required_level": "admin"},
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> Dict[str, str]:
    """Retrieve user data safely.

    Raises:
        KeyError: If the user_id does not exist.
    """
    return USERS[user_id]


def _get_content(item_id: int) -> Dict[str, str]:
    """Retrieve content data safely.

    Raises:
        KeyError: If the item_id does not exist.
    """
    return CONTENT[item_id]


# --------------------------------------------------------------------------- #
# Main access control function
# --------------------------------------------------------------------------- #

def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine whether a user can access a piece of content.

    Admin users are granted unrestricted access.  Regular users may only
    access content whose required subscription level matches or is lower
    than their own.  The function returns the title of the content if
    access is allowed, otherwise it returns 'Access Denied'.

    Args:
        user_id (int): The ID of the user attempting access.
        item_id (int): The ID of the content being requested.

    Returns:
        str: The title of the content if access is granted, or
             'Access Denied' otherwise.

    Raises:
        KeyError: If either the user_id or item_id is not found in the
                  corresponding dictionaries.
    """
    # Fetch user and content records
    try:
        user = _get_user(user_id)
        content = _get_content(item_id)
    except KeyError as exc:
        # Propagate the error with a clear message
        raise KeyError(f"Invalid identifier: {exc}") from exc

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Define a simple hierarchy for subscription levels
    level_hierarchy = {"basic": 1, "premium": 2}

    user_level_value = level_hierarchy.get(user["subscription_level"])
    content_level_value = level_hierarchy.get(content["required_level"])

    # If the required level is not recognized, deny access
    if user_level_value is None or content_level_value is None:
        return "Access Denied"

    # Grant access only if user's level >= required level
    if user_level_value >= content_level_value:
        return content["title"]

    # Default denial
    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample test cases
    tests = [
        (1, 101),  # admin to basic content
        (2, 102),  # basic user to premium content
        (3, 102),  # premium user to premium content
        (2, 103),  # basic user to admin guide
    ]

    for uid, cid in tests:
        try:
            result = grant_access(uid, cid)
            print(f"User {uid} accessing item {cid}: {result}")
        except KeyError as e:
            print(f"User {uid} accessing item {cid}: Error - {e}")