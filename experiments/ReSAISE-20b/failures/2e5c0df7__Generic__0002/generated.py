# -*- coding: utf-8 -*-
"""
Utility to retrieve content titles based on user access rights.
"""

from typing import Dict, Any

# Example data structures. In a real application these would be loaded from
# a database or another persistence layer.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

# Mapping of content IDs to a dictionary containing the title and
# the minimum subscription tier required for access.
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Guide", "required_tier": "basic"},
    102: {"title": "Premium Workshop", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": "admin"},  # only admins
}

# Define the order of subscription tiers for comparison.
TIER_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    "admin": 3,  # administrators are treated as a higher tier
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.
    """
    # Retrieve user and item safely
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    item = CONTENT.get(item_id)
    if not item:
        return "Access Denied"

    # Administrators have unrestricted access
    if user.get("role") == "admin":
        return item["title"]

    # For regular users, compare subscription tiers
    user_tier = user.get("subscription_tier")
    required_tier = item.get("required_tier")

    # Resolve tier levels; if a tier is missing, deny access
    user_level = TIER_HIERARCHY.get(user_tier)
    required_level = TIER_HIERARCHY.get(required_tier)

    if user_level is None or required_level is None:
        return "Access Denied"

    # User can access if their tier level meets or exceeds the requirement
    if user_level >= required_level:
        return item["title"]

    return "Access Denied"