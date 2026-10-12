# -*- coding: utf-8 -*-

"""
Access control module for content delivery.
"""

from typing import Dict

# Example user database
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

# Example content database
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Premium Guide", "required_level": "premium"},
    103: {"title": "Admin Manual", "required_level": "admin"},
}

# Define a numeric hierarchy for subscription levels
LEVEL_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    # Admin is handled separately
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Return the content title if the user is allowed to access it.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content data
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If the content requires admin only, deny non-admins
    if required_level == "admin":
        return "Access Denied"

    # Compare subscription levels
    user_rank = LEVEL_HIERARCHY.get(user_level, 0)
    required_rank = LEVEL_HIERARCHY.get(required_level, 0)

    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"


# Example usage
if __name__ == "__main__":
    print(grant_access(1, 102))  # Admin access
    print(grant_access(2, 101))  # Basic user accessing basic content
    print(grant_access(2, 102))  # Basic user denied premium content