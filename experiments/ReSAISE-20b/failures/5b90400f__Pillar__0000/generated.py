# -*- coding: utf-8 -*-
"""
Access control module for content retrieval.

This module defines the `access_content` function which checks whether a user
is authorized to view a given piece of content.  Admin users have full access,
while regular users may only view content that matches their subscription
level.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data structures (replace with real database lookups in production)
# --------------------------------------------------------------------------- #

USERS = {
    # user_id: {"role": "admin" | "user", "subscription_level": str}
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT = {
    # content_id: {"required_subscription": str, "data": any}
    101: {"required_subscription": "basic",   "data": "Basic content A"},
    102: {"required_subscription": "premium", "data": "Premium content B"},
    103: {"required_subscription": "basic",   "data": "Basic content C"},
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> dict | None:
    """Retrieve user record by ID, or None if not found."""
    return USERS.get(user_id)


def _get_content(content_id: int) -> dict | None:
    """Retrieve content record by ID, or None if not found."""
    return CONTENT.get(content_id)


def _is_authorized(user: dict, content: dict) -> bool:
    """
    Determine if the user is authorized to access the content.

    Admins have unrestricted access. Regular users may only view content
    whose required subscription matches their own.
    """
    if user["role"] == "admin":
        return True
    # For normal users, compare subscription levels.
    return user["subscription_level"] == content["required_subscription"]


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def access_content(current_user_id: int, content_id: int) -> any:
    """
    Return the requested content data if the current user is authorized.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access content.
    content_id : int
        The ID of the content to be accessed.

    Returns
    -------
    any | str
        Content data if authorized, otherwise the string 'Access Denied'.

    Raises
    ------
    TypeError
        If either argument is not an integer.
    ValueError
        If the user or content does not exist in the data store.
    """
    # Input validation
    if not isinstance(current_user_id, int):
        raise TypeError("current_user_id must be an integer")
    if not isinstance(content_id, int):
        raise TypeError("content_id must be an integer")

    user = _get_user(current_user_id)
    if user is None:
        raise ValueError(f"User with ID {current_user_id} not found")

    content = _get_content(content_id)
    if content is None:
        raise ValueError(f"Content with ID {content_id} not found")

    if _is_authorized(user, content):
        return content["data"]

    return "Access Denied"