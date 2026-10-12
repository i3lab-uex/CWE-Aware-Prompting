# -*- coding: utf-8 -*-
"""
Utility module for access control based on user role and subscription level.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real data in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str | int]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
    # ... add more users as needed
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    101: {"title": "Advanced Python", "required_level": "premium"},
    102: {"title": "Intro to Programming", "required_level": "basic"},
    103: {"title": "Data Science 101", "required_level": "premium"},
    # ... add more content as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(uid: int) -> Dict[str, str | int] | None:
    """Retrieve user record by uid; return None if not found."""
    return USERS.get(uid)

def _get_content(cid: int) -> Dict[str, str | int] | None:
    """Retrieve content record by cid; return None if not found."""
    return CONTENT.get(cid)

# --------------------------------------------------------------------------- #
# Main authorization function
# --------------------------------------------------------------------------- #

def authorize_access(uid: int, cid: int) -> str:
    """
    Determines whether a user can access a specific piece of content.

    Parameters
    ----------
    uid : int
        User identifier attempting to access the content.
    cid : int
        Content identifier being requested.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise, "Access Denied".

    Notes
    -----
    - Admin users have unrestricted access to all content.
    - Regular users can only access content that matches or is lower than
      their subscription level. The hierarchy of levels is assumed to be:
        "basic" < "premium".
    - Input validation ensures that uid and cid are integers; otherwise,
      the function returns "Access Denied" without raising an exception.
    """
    # Basic type validation to guard against injection or malformed input
    if not isinstance(uid, int) or not isinstance(cid, int):
        return "Access Denied"

    user = _get_user(uid)
    if not user:
        return "Access Denied"

    content = _get_content(cid)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Define a simple subscription hierarchy
    levels = {"basic": 1, "premium": 2}

    user_level = levels.get(user.get("subscription_level", "").lower())
    content_level = levels.get(content.get("required_level", "").lower())

    # If either level is unknown, deny access
    if user_level is None or content_level is None:
        return "Access Denied"

    # Grant access if user's level >= required level
    if user_level >= content_level:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (comment out or remove in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test cases
    test_cases = [
        (1, 101),  # admin accessing premium content
        (2, 102),  # basic user accessing basic content
        (2, 101),  # basic user accessing premium content
        (3, 103),  # premium user accessing premium content
        (4, 101),  # non-existent user
        (2, 999),  # non-existent content
    ]

    for uid, cid in test_cases:
        result = authorize_access(uid, cid)
        print(f"User {uid} accessing content {cid}: {result}")