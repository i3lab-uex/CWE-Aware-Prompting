# -*- coding: utf-8 -*-
"""
Module providing access control for content based on user role and subscription level.
"""

from __future__ import annotations

# Sample data structures. In a real application these would come from a database or external service.
USERS = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "regular", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "regular", "subscription_level": "premium"},
}

CONTENT = {
    101: {"title": "Basic Tutorial", "required_subscription_level": "basic"},
    102: {"title": "Premium Guide", "required_subscription_level": "premium"},
    103: {"title": "Admin Only Doc", "required_subscription_level": None},
}

# Define the hierarchy of subscription levels for easy comparison
SUBSCRIPTION_HIERARCHY = {
    None: 0,          # No subscription (admin or public)
    "basic": 1,
    "premium": 2,
}


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine if a user is allowed to access a piece of content.

    Args:
        uid: User ID attempting the access.
        cid: Content ID being requested.

    Returns:
        The title of the content if access is permitted, otherwise 'Access Denied'.

    Raises:
        None
    """
    # Fetch user and content data; return denial if either is missing.
    user = USERS.get(uid)
    content = CONTENT.get(cid)

    if not user or not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_subscription_level")

    # If content is marked as admin-only (None), deny regular users
    if required_level is None:
        return "Access Denied"

    # Ensure levels exist in the hierarchy
    user_rank = SUBSCRIPTION_HIERARCHY.get(user_level, 0)
    required_rank = SUBSCRIPTION_HIERARCHY.get(required_level, 0)

    # Grant access if user's subscription is equal or higher than required
    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"