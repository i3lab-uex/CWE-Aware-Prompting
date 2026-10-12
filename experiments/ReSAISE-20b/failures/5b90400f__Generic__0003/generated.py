# -*- coding: utf-8 -*-
"""
Content access control module.

The module defines a single function `access_content` that checks whether a
user is allowed to view a piece of content based on the user's role and
subscription level.  Admins can access all content, while regular users can
only view content that matches their subscription tier.

The data structures `USERS` and `CONTENT` are defined below as examples.
In a real application they would be populated from a database or external
service.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data structures.  In production these would come from a database.
# --------------------------------------------------------------------------- #

USERS = {
    # user_id : {role: str, subscription: str}
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

CONTENT = {
    # content_id : {"data": Any, "required_subscription": str}
    101: {"data": "Premium article on AI", "required_subscription": "gold"},
    102: {"data": "Standard article on web dev", "required_subscription": "silver"},
    103: {"data": "Basic article on Python", "required_subscription": "bronze"},
    104: {"data": "Open content for all", "required_subscription": None},  # accessible to everyone
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> dict:
    """
    Retrieve user information from the USERS dictionary.

    Raises:
        KeyError: If the user_id does not exist.
    """
    return USERS[user_id]


def _get_content(content_id: int) -> dict:
    """
    Retrieve content information from the CONTENT dictionary.

    Raises:
        KeyError: If the content_id does not exist.
    """
    return CONTENT[content_id]


def _subscription_rank(sub: str | None) -> int:
    """
    Convert subscription level to an integer rank for comparison.

    Higher numbers mean higher privileges.  `None` is treated as the lowest
    rank (accessible to everyone).
    """
    order = {"bronze": 1, "silver": 2, "gold": 3}
    return order.get(sub, 0)


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def access_content(current_user_id: int, content_id: int):
    """
    Return the content data if the user is authorized; otherwise return
    'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access content.
    content_id : int
        The identifier of the content being accessed.

    Returns
    -------
    Any | str
        The content data if authorized, otherwise the string 'Access Denied'.

    Raises
    ------
    KeyError
        If either the user or content does not exist in the dictionaries.
    """
    # Retrieve user and content data
    user = _get_user(current_user_id)
    content = _get_content(content_id)

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["data"]

    # For regular users, compare subscription ranks
    required = content.get("required_subscription")
    if required is None:
        # Public content, no subscription needed
        return content["data"]

    user_rank = _subscription_rank(user.get("subscription"))
    required_rank = _subscription_rank(required)

    if user_rank >= required_rank:
        return content["data"]

    # If none of the above conditions are met, deny access
    return "Access Denied"