# -*- coding: utf-8 -*-
"""
Authorisation helper for content access.

This module defines the `fetch_content` function which checks whether a user
is allowed to view a piece of content based on their role and subscription level.
"""

from typing import Dict, Any

# Sample data structures. In a real application these would come from a
# database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription_level: int}
    1: {"role": "admin", "subscription_level": 5},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 3},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_level: int}
    101: {"title": "Basic Guide", "required_level": 1},
    102: {"title": "Intermediate Tutorial", "required_level": 2},
    103: {"title": "Advanced Techniques", "required_level": 4},
}


def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    permissions, otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    cid : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate input types to avoid accidental misuse
    if not isinstance(user_id, int) or not isinstance(cid, int):
        return "Access Denied"

    # Retrieve user and content data
    user = USERS.get(user_id)
    content = CONTENT.get(cid)

    # If either the user or content does not exist, deny access
    if user is None or content is None:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level >= required_level
    user_level = user.get("subscription_level", 0)
    required_level = content.get("required_level", float("inf"))

    if user_level >= required_level:
        return content["title"]

    # All other cases are denied
    return "Access Denied"


# Example usage (for demonstration; remove or guard under __name__ == "__main__" in production)
if __name__ == "__main__":
    print(fetch_content(1, 103))  # Admin: Advanced Techniques
    print(fetch_content(2, 102))  # Not enough level: Access Denied
    print(fetch_content(3, 101))  # Level 3 user accessing level 1 content: Basic Guide