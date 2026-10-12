# -*- coding: utf-8 -*-
"""
Module providing access control for content based on user role and subscription level.
"""

from typing import Dict

# Sample data structures (in a real system these would be fetched from a database)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user",  "subscription_level": "basic"},
    3: {"role": "user",  "subscription_level": "premium"},
}

# Mapping of content IDs to required subscription levels
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Article",     "required_level": "basic"},
    102: {"title": "Premium Video",     "required_level": "premium"},
    103: {"title": "Admin Report",      "required_level": "admin"},
}

# Define a simple hierarchy for subscription levels
LEVEL_ORDER = {"basic": 1, "premium": 2, "admin": 3}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine if a user has access to a given content item.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the content item.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    - Admin users bypass subscription checks entirely.
    - Regular users must have a subscription level that is >= the content's required level.
    """
    # Fetch user and item data
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    item = CONTENT.get(item_id)
    if not item:
        return "Access Denied"

    # Admin role bypasses subscription checks
    if user.get("role") == "admin":
        return item["title"]

    # Determine numeric levels for comparison
    user_level = LEVEL_ORDER.get(user.get("subscription_level", "").lower(), 0)
    required_level = LEVEL_ORDER.get(item.get("required_level", "").lower(), 0)

    if user_level >= required_level:
        return item["title"]

    return "Access Denied"