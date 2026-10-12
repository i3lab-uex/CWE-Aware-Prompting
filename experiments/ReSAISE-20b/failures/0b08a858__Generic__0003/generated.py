# view_content.py

"""
Author: OpenAI ChatGPT
Description:
    Function to control access to content based on user role and subscription tier.
"""

from typing import Dict, Any

# Example data structures (in practice these would be loaded from a database or config)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, tier: str}
    1: {"role": "admin", "tier": "premium"},
    2: {"role": "user", "tier": "basic"},
    3: {"role": "user", "tier": "premium"},
}

# Content mapping: content_id -> {title: str, required_tier: str}
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Tutorial", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Enterprise Overview", "required_tier": "enterprise"},
}

# Define a simple tier hierarchy for comparison
TIER_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    "enterprise": 3
}


def _get_user(user_id: int) -> Dict[str, Any]:
    """
    Safely retrieve a user dictionary. Raises KeyError if the user does not exist.
    """
    return USERS[user_id]


def _get_content(content_id: int) -> Dict[str, Any]:
    """
    Safely retrieve a content dictionary. Raises KeyError if the content does not exist.
    """
    return CONTENT[content_id]


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Returns the content title if the user has permission to view it.
    Otherwise returns 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content being accessed.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content does not exist.
    """
    # Retrieve user and resource information
    user = _get_user(actor_user_id)
    content = _get_content(resource_id)

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a tier equal or higher than required
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # Validate tiers exist in the hierarchy
    if user_tier not in TIER_HIERARCHY or required_tier not in TIER_HIERARCHY:
        # Unknown tier – deny access to avoid privilege escalation
        return "Access Denied"

    if TIER_HIERARCHY[user_tier] >= TIER_HIERARCHY[required_tier]:
        return content["title"]

    return "Access Denied"