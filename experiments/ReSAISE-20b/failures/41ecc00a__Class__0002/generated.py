# -*- coding: utf-8 -*-

"""
Security-aware implementation of content retrieval with proper authorization checks.
"""

from typing import Dict

# Sample data structures. In a real application these would be loaded from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python", "required_tier": "premium"},
    102: {"title": "Intro to Programming", "required_tier": "basic"},
    103: {"title": "Data Science Basics", "required_tier": "premium"},
}

# Define the order of subscription tiers for comparison
TIER_ORDER = {"basic": 1, "premium": 2}


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Retrieve the title of the requested content if the user has sufficient
    privileges. Administrators can access all content; regular users must have
    a subscription tier equal to or higher than the required tier.

    Parameters:
        user_id (int): Identifier of the requesting user.
        content_id (int): Identifier of the requested content.

    Returns:
        str: The content title if access is granted; otherwise 'Access Denied'.

    Raises:
        KeyError: If the user_id or content_id does not exist in their respective
                  dictionaries.
    """
    # Validate existence of user and content
    if user_id not in USERS:
        raise KeyError(f"User ID {user_id} not found.")
    if content_id not in CONTENT:
        raise KeyError(f"Content ID {content_id} not found.")

    user = USERS[user_id]
    content = CONTENT[content_id]

    # Administrator bypasses tier checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription tiers
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # Ensure tiers are defined and comparable
    if user_tier not in TIER_ORDER or required_tier not in TIER_ORDER:
        return "Access Denied"

    if TIER_ORDER[user_tier] >= TIER_ORDER[required_tier]:
        return content["title"]

    return "Access Denied"