# -*- coding: utf-8 -*-
"""
Content retrieval with proper authorization checks.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": None},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": None},
}


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Retrieve the title of a piece of content if the user has permission.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title if authorized, otherwise "Access Denied".
    """
    # Validate input types to avoid injection or accidental misuse
    if not isinstance(user_id, int) or not isinstance(content_id, int):
        return "Access Denied"

    user = USERS.get(user_id)
    content = CONTENT.get(content_id)

    # If either the user or the content does not exist, deny access
    if user is None or content is None:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription tiers
    required_tier = content.get("required_tier")
    user_tier = user.get("subscription_tier")

    # If content is public (no required tier) or tiers match, grant access
    if required_tier is None:
        return content["title"]

    if user_tier == required_tier:
        return content["title"]

    # All other cases result in denial
    return "Access Denied"