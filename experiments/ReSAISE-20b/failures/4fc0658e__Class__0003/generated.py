# -*- coding: utf-8 -*-
"""
Utility module for content access control.
"""

from typing import Dict

# Example data structures. In a real application these would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Open Access Article", "required_level": "basic"},
    102: {"title": "Premium Report", "required_level": "premium"},
    103: {"title": "Admin Only Briefing", "required_level": "admin"},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user has permission to access it.
    Otherwise, return 'Access Denied'.

    Args:
        given_user_id (int): ID of the user attempting to access content.
        target_content_id (int): ID of the content being requested.

    Raises:
        KeyError: If either user or content does not exist.
    """
    # Validate that the user exists
    if given_user_id not in USERS:
        raise KeyError(f"User ID {given_user_id} not found.")

    # Validate that the content exists
    if target_content_id not in CONTENT:
        raise KeyError(f"Content ID {target_content_id} not found.")

    user = USERS[given_user_id]
    content = CONTENT[target_content_id]

    # Admins have full access
    if user["role"] == "admin":
        return content["title"]

    # Regular users must have a subscription level that meets or exceeds the requirement
    required_level = content["required_level"]

    # Define a simple hierarchy for subscription levels
    level_hierarchy = {"basic": 1, "premium": 2}

    user_level_value = level_hierarchy.get(user["subscription_level"], 0)
    required_level_value = level_hierarchy.get(required_level, 0)

    if user_level_value >= required_level_value:
        return content["title"]

    # If none of the above conditions are met, deny access
    return "Access Denied"