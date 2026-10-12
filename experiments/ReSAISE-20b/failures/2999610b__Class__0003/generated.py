# -*- coding: utf-8 -*-

"""
Module providing access control for content based on user roles and subscription levels.
"""

# Example data structures. In real usage these would be imported from a database or
# configuration module.
USERS = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "standard"},
}

CONTENT = {
    101: {"title": "Advanced Python", "required_subscription": "premium"},
    102: {"title": "Intro to Programming", "required_subscription": "basic"},
    103: {"title": "Data Science Basics", "required_subscription": "standard"},
}

# Defines the order of subscription levels from lowest to highest.
subscription_hierarchy = ["basic", "standard", "premium"]


def _level_index(level: str) -> int:
    """
    Helper that returns the index of a subscription level in the hierarchy.
    Raises ValueError if the level is unknown.
    """
    try:
        return subscription_hierarchy.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Returns the title of a content item if the user has sufficient permissions,
    otherwise returns 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access the content.
    contid : int
        The ID of the content item.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.
    """
    # Validate existence of user and content entries
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(contid)
    if not content:
        return "Access Denied"

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription level
    user_level = user.get("subscription")
    required_level = content.get("required_subscription")

    if not user_level or not required_level:
        return "Access Denied"

    try:
        user_idx = _level_index(user_level)
        required_idx = _level_index(required_level)
    except ValueError:
        # If either level is unknown, deny access to avoid privilege escalation
        return "Access Denied"

    # Grant access only if user's level is equal or higher than required
    return content["title"] if user_idx >= required_idx else "Access Denied"