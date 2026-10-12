# -*- coding: utf-8 -*-
"""
A small module that controls content access based on user subscription levels.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from
# a database or an external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": None},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Tutorial", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": None},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the content title if the user has permission to access it,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the requested content.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.
    """
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        content = CONTENT.get(item_id)
        return content["title"] if content else "Access Denied"

    # Regular users must have a subscription tier
    user_tier = user.get("subscription_tier")
    if not user_tier:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    required_tier = content.get("required_tier")
    # If the content does not require a tier, grant access
    if required_tier is None:
        return content["title"]

    # Allow access only if the user's tier matches or exceeds the required tier
    tiers = ["basic", "premium"]  # Ordered from lowest to highest
    try:
        user_index = tiers.index(user_tier)
        required_index = tiers.index(required_tier)
    except ValueError:
        return "Access Denied"

    if user_index >= required_index:
        return content["title"]

    return "Access Denied"