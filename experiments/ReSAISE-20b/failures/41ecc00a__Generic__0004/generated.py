# -*- coding: utf-8 -*-
"""
Utility for accessing content based on user subscription and role.
"""

from __future__ import annotations
from typing import Dict, Any

# Example data structures. In a real application these would come from
# a database or external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_tier": "gold"},
    2: {"role": "user", "subscription_tier": "silver"},
    3: {"role": "user", "subscription_tier": "bronze"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Advanced Python", "required_tier": "gold"},
    102: {"title": "Intro to JavaScript", "required_tier": "silver"},
    103: {"title": "Basic HTML", "required_tier": "bronze"},
}

# Define a simple hierarchy for subscription tiers to allow comparison.
TIER_ORDER = {
    "bronze": 1,
    "silver": 2,
    "gold": 3,
}


def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Determine if a user has access to the given content.

    Parameters
    ----------
    user : dict
        Dictionary containing at least 'role' and 'subscription_tier'.
    content : dict
        Dictionary containing at least 'required_tier'.

    Returns
    -------
    bool
        True if the user can access the content, False otherwise.
    """
    # Admins have unrestricted access
    if user.get("role") == "admin":
        return True

    # Regular users must have a subscription tier that meets or exceeds the
    # required level for the content.
    user_tier = TIER_ORDER.get(user.get("subscription_tier", "").lower())
    content_tier = TIER_ORDER.get(content.get("required_tier", "").lower())

    if user_tier is None or content_tier is None:
        # If either tier is unknown, deny access for safety.
        return False

    return user_tier >= content_tier


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Retrieve the title of a piece of content if the user has permission.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    content_id : int
        Identifier of the content the user is trying to access.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise "Access Denied".

    Raises
    ------
    KeyError
        If either the user_id or content_id does not exist in the respective dictionaries.
    """
    # Fetch user and content data; raise KeyError if not found
    user = USERS[user_id]
    content = CONTENT[content_id]

    if _has_access(user, content):
        return content["title"]

    return "Access Denied"