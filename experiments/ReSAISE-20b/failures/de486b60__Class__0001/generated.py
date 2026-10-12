# -*- coding: utf-8 -*-

"""
Authorization module for content access.

This module defines a simple in‑memory representation of users and
content, and implements the `view_content` function that checks a
user's role and subscription level before granting access.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Sample data structures
# ----------------------------------------------------------------------


# Users dictionary:
#   key   -> user ID (int)
#   value -> dict with 'role' and 'subscription'
USERS: dict[int, dict[str, str]] = {
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
    4: {"role": "user", "subscription": "gold"},
}

# Content dictionary:
#   key   -> content ID (int)
#   value -> dict with 'title' and required 'subscription'
CONTENT: dict[int, dict[str, str]] = {
    101: {"title": "Premium Article", "subscription": "gold"},
    102: {"title": "Silver News", "subscription": "silver"},
    103: {"title": "Bronze Update", "subscription": "bronze"},
    104: {"title": "General Post", "subscription": "free"},
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def _get_user(uid: int) -> dict[str, str]:
    """Retrieve user record or raise an error if the user does not exist."""
    try:
        return USERS[uid]
    except KeyError as exc:
        raise ValueError(f"Unknown user ID: {uid}") from exc


def _get_content(cont_id: int) -> dict[str, str]:
    """Retrieve content record or raise an error if the content does not exist."""
    try:
        return CONTENT[cont_id]
    except KeyError as exc:
        raise ValueError(f"Unknown content ID: {cont_id}") from exc


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has sufficient
    privileges, otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to access the content.
    cont_id : int
        The ID of the requested content.

    Returns
    -------
    str
        Content title if authorized, otherwise 'Access Denied'.

    Raises
    ------
    ValueError
        If either the user ID or content ID is not known.
    """
    # Retrieve records (will raise ValueError if missing)
    user = _get_user(uid)
    content = _get_content(cont_id)

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level equal to or higher
    # than the content's required level. For simplicity, we use a
    # defined hierarchy.
    subscription_order = {"free": 0, "bronze": 1, "silver": 2, "gold": 3}

    user_level = subscription_order.get(user["subscription"], -1)
    content_level = subscription_order.get(content["subscription"], -1)

    if user_level >= content_level:
        return content["title"]

    # If none of the above conditions are met, deny access
    return "Access Denied"