# -*- coding: utf-8 -*-

"""
Content access control module.

Author: <Your Name>
"""

from typing import Dict

# Example data structures. In a real application these would be populated
# from a database or another persistent store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

# Each content item requires a minimum subscription tier to access.
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial", "required_tier": "basic"},
    102: {"title": "Advanced Guide", "required_tier": "premium"},
}

# Define the hierarchy of subscription tiers for comparison.
TIER_HIERARCHY = {"basic": 1, "premium": 2}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the content the user is trying to access.

    Returns
    -------
    str
        Content title if authorized, otherwise 'Access Denied'.
    """
    # Retrieve user and content records.
    user = USERS.get(active_user_id)
    content_item = CONTENT.get(item_id)

    # If either the user or the content item does not exist,
    # deny access. This also protects against tampering with IDs.
    if user is None or content_item is None:
        return "Access Denied"

    # Admins bypass all checks.
    if user.get("role") == "admin":
        return content_item["title"]

    # For regular users, compare subscription tiers.
    user_tier = user.get("subscription_tier")
    required_tier = content_item.get("required_tier")

    # If either tier is missing or unrecognized, deny access.
    if (
        user_tier not in TIER_HIERARCHY
        or required_tier not in TIER_HIERARCHY
    ):
        return "Access Denied"

    # Grant access only if the user's tier is equal or higher.
    if TIER_HIERARCHY[user_tier] >= TIER_HIERARCHY[required_tier]:
        return content_item["title"]

    # All other cases result in denial.
    return "Access Denied"