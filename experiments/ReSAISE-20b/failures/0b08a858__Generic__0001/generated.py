# view_content.py

from typing import Dict, Any

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Tutorial", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": "admin_only"},
}

# Define subscription hierarchy for comparison
TIER_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    "admin_only": 3,   # highest level, only admins should access
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the content title if the user has permission, otherwise 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        The ID of the user attempting to access content.
    resource_id : int
        The ID of the content being accessed.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content safely; return denied if not found
    user = USERS.get(actor_user_id)
    resource = CONTENT.get(resource_id)

    if not user or not resource:
        return "Access Denied"

    # Admins can access everything
    if user.get("role") == "admin":
        return resource["title"]

    # For regular users, compare subscription tiers
    user_tier = user.get("subscription_tier")
    required_tier = resource.get("required_tier")

    # Map tiers to numeric levels; if unknown, deny access
    user_level = TIER_HIERARCHY.get(user_tier)
    required_level = TIER_HIERARCHY.get(required_tier)

    if user_level is None or required_level is None:
        return "Access Denied"

    # User can access if their tier level >= required
    if user_level >= required_level:
        return resource["title"]

    return "Access Denied"