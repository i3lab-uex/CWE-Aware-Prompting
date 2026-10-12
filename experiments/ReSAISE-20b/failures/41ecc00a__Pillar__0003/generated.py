# -*- coding: utf-8 -*-

"""
retrieve_content module

This module provides a single function `retrieve_content` that controls
access to content items based on user role and subscription tier.
It protects against improper access control (CWE-284) by ensuring
that only administrators or users whose subscription level meets or
exceeds the required level for a content item can retrieve it.
"""

from typing import Dict

# Sample data structures (these would normally come from a database)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

# Subscription levels in ascending order of privilege
SUBSCRIPTION_HIERARCHY = {
    "basic": 1,
    "standard": 2,
    "premium": 3,
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Article", "required_tier": "basic"},
    102: {"title": "Standard Video", "required_tier": "standard"},
    103: {"title": "Premium Report", "required_tier": "premium"},
}


def _get_user(user_id: int) -> Dict[str, str]:
    """
    Retrieve user data safely. Raises KeyError if the user does not exist.
    """
    try:
        return USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} not found") from exc


def _get_content(content_id: int) -> Dict[str, str]:
    """
    Retrieve content data safely. Raises KeyError if the content does not exist.
    """
    try:
        return CONTENT[content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {content_id} not found") from exc


def _has_access(user: Dict[str, str], content: Dict[str, str]) -> bool:
    """
    Determine whether a user is authorized to access the given content.
    Administrators have full access. For regular users, compare subscription
    tiers using a defined hierarchy to avoid direct string comparison.
    """
    # Admins bypass all checks
    if user.get("role") == "admin":
        return True

    # Resolve subscription levels
    user_level = SUBSCRIPTION_HIERARCHY.get(user.get("subscription_tier"))
    content_level = SUBSCRIPTION_HIERARCHY.get(content.get("required_tier"))

    # If either tier is unknown, deny access to be safe
    if user_level is None or content_level is None:
        return False

    # User must have a level equal to or higher than required
    return user_level >= content_level


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    content_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.
    """
    try:
        user = _get_user(user_id)
        content = _get_content(content_id)

        if _has_access(user, content):
            return content["title"]
    except KeyError:
        # Either user or content not found; treat as denied access
        pass

    return "Access Denied"