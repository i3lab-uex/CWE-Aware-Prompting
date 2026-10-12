# -*- coding: utf-8 -*-

"""
Utility module for content access control.

The function `fetch_content` enforces subscription-based access to
content items.  Administrators bypass all checks and receive every
item, while regular users are restricted to content that matches or
is lower than their subscription tier.

The implementation follows the principle of least privilege and uses
immutable data structures to avoid accidental modification.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, sub_level: int}
    1: {"role": "admin", "sub_level": 5},
    2: {"role": "user", "sub_level": 3},
    3: {"role": "user", "sub_level": 1},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_level: int}
    101: {"title": "Premium Article", "required_level": 3},
    102: {"title": "Basic Tutorial", "required_level": 1},
    103: {"title": "Admin Guide", "required_level": 5},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has
    sufficient permissions, otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting access.
    cid : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.
    """
    # Retrieve user and content safely
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required level
    user_level = user.get("sub_level", 0)
    required_level = content.get("required_level", float("inf"))

    if user_level >= required_level:
        return content["title"]

    # If none of the above, deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin
        (2, 101),  # user with sufficient level
        (3, 101),  # user below required level
        (2, 999),  # non-existent content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {fetch_content(uid, cid)}")