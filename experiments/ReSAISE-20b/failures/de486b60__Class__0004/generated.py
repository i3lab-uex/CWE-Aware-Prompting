# -*- coding: utf-8 -*-
"""
Content access control module.

Provides the `view_content` function which checks a user's role and
subscription level before granting access to requested content.
"""

from __future__ import annotations

# Sample data. In a real application these would come from a database.
USERS = {
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

# Subscription levels are ordered from lowest to highest.
SUBSCRIPTION_ORDER = {"basic": 1, "premium": 2}

CONTENT = {
    101: {"title": "Basic Article", "required_level": "basic"},
    102: {"title": "Premium Guide", "required_level": "premium"},
    103: {"title": "Admin Manual", "required_level": None},
}


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    uid : int
        User ID attempting to access the content.
    cont_id : int
        Content ID that the user wants to view.

    Returns
    -------
    str
        The content title or 'Access Denied'.
    """
    # Basic input validation: ensure user and content exist
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level that meets or exceeds
    # the content's required level.
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If the content has no level requirement, allow access to all users
    if required_level is None:
        return content["title"]

    # If the user has no subscription level (e.g., guest), deny access
    if not user_level:
        return "Access Denied"

    # Compare subscription levels using the defined order
    user_rank = SUBSCRIPTION_ORDER.get(user_level, 0)
    required_rank = SUBSCRIPTION_ORDER.get(required_level, 0)

    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"