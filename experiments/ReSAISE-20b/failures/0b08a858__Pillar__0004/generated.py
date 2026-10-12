# -*- coding: utf-8 -*-
"""
Secure content access module.
"""

from typing import Dict

# Sample data structures (replace with actual data sources in production)
USERS: Dict[int, Dict[str, str]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"content_id": 101, "title": "Premium Article", "required_tier": "premium"},
    102: {"content_id": 102, "title": "Basic Article", "required_tier": "basic"},
    103: {"content_id": 103, "title": "Public Post", "required_tier": "public"},
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Returns the title of the requested content if the user has access.
    Otherwise returns 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Fetch user and content safely; use get to avoid KeyError
    user = USERS.get(actor_user_id)
    resource = CONTENT.get(resource_id)

    # If either the user or content does not exist, deny access
    if user is None or resource is None:
        return "Access Denied"

    # Admin users bypass tier checks
    if user.get("role", "").lower() == "admin":
        return resource["title"]

    # Normal users: compare subscription tiers
    user_tier = user.get("subscription_tier", "").lower()
    required_tier = resource.get("required_tier", "").lower()

    # Define tier hierarchy for comparison
    tier_order = {"public": 0, "basic": 1, "premium": 2}

    # If required tier is not defined or unknown, deny access
    if required_tier not in tier_order:
        return "Access Denied"

    # Grant access only if user's tier level is >= required
    if tier_order.get(user_tier, -1) >= tier_order[required_tier]:
        return resource["title"]

    return "Access Denied"