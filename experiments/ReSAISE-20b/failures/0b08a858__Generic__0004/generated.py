# -*- coding: utf-8 -*-
"""
Implementation of a content access control function.
"""

from typing import Dict

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_tier": "gold"},
    2: {"role": "user", "subscription_tier": "silver"},
    3: {"role": "user", "subscription_tier": "bronze"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Premium Article", "required_tier": "gold"},
    102: {"title": "Silver News", "required_tier": "silver"},
    103: {"title": "Bronze Blog", "required_tier": "bronze"},
    104: {"title": "Public Post", "required_tier": "free"},
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the content title if the user has permission to view it,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user attempting to access content.
    resource_id : int
        The ID of the requested content.

    Returns
    -------
    str
        Content title if access granted, else 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or resource ID does not exist in their respective dictionaries.
    """
    # Validate existence of the user and content
    try:
        user = USERS[actor_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {actor_user_id} not found.") from exc

    try:
        content = CONTENT[resource_id]
    except KeyError as exc:
        raise KeyError(f"Resource ID {resource_id} not found.") from exc

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required tier
    user_tier = user.get("subscription_tier", "free")
    required_tier = content.get("required_tier", "free")

    # Define tier hierarchy for comparison
    tiers = {"free": 0, "bronze": 1, "silver": 2, "gold": 3}

    if tiers.get(user_tier, -1) >= tiers.get(required_tier, -1):
        return content["title"]

    # Access denied for insufficient tier
    return "Access Denied"