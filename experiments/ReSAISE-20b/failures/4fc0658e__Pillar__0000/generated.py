# -*- coding: utf-8 -*-
"""
Secure content access module.
"""

from typing import Dict

# Example data structures (in a real system these would be fetched from a database)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Premium Guide", "required_level": "premium"},
    103: {"title": "Admin Manual", "required_level": "admin"},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    Otherwise return 'Access Denied'.

    Args:
        given_user_id: ID of the user attempting access.
        target_content_id: ID of the content to be accessed.

    Returns:
        str: Content title or 'Access Denied'.
    """
    # Validate inputs are integers to avoid type confusion
    if not isinstance(given_user_id, int) or not isinstance(target_content_id, int):
        return "Access Denied"

    user = USERS.get(given_user_id)
    content = CONTENT.get(target_content_id)

    # If either user or content does not exist, deny access
    if user is None or content is None:
        return "Access Denied"

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, check subscription level
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Map levels to a numeric hierarchy for comparison
    level_order = {"basic": 1, "premium": 2, "admin": 3}
    if level_order.get(user_level, 0) >= level_order.get(required_level, 0):
        return content["title"]

    # All other cases are denied
    return "Access Denied"