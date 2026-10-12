# -*- coding: utf-8 -*-
"""
Content access control module.

Provides a single function `fetch_content` that returns the title of a
content item if the requesting user has sufficient privileges.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

# Example user database. In a real system this would be replaced with a
# persistent store or an external authentication service.
USERS = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
    4: {"role": "user", "subscription": "basic"},
}

# Content database mapping content id to a dict containing the title and
# the minimum subscription level required.
CONTENT = {
    101: {"title": "Welcome Guide", "level": "basic"},
    102: {"title": "Advanced Topics", "level": "premium"},
    103: {"title": "Admin Manual", "level": "admin"},
}

# Ordered list of subscription tiers for comparison.
SUBSCRIPTION_ORDER = ["basic", "premium"]


def _has_access(user: dict, content_level: str) -> bool:
    """
    Determine whether a user has permission to view content of the given
    subscription level.

    Parameters
    ----------
    user : dict
        User record containing at least 'role' and optionally 'subscription'.
    content_level : str
        The subscription level required for the requested content.

    Returns
    -------
    bool
        True if access is granted, False otherwise.
    """
    # Administrators bypass all checks
    if user.get("role") == "admin":
        return True

    # If the content is explicitly for admins only
    if content_level == "admin":
        return False

    user_level = user.get("subscription")
    if user_level is None:
        return False  # non‑admin users must have a subscription level

    try:
        user_idx = SUBSCRIPTION_ORDER.index(user_level)
        content_idx = SUBSCRIPTION_ORDER.index(content_level)
    except ValueError:
        # Unknown subscription level in either user or content
        return False

    return user_idx >= content_idx


def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of a content item if the user is permitted to view it.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise
        'Access Denied'.

    Notes
    -----
    - If either the user or content id is not present in the database,
      access is denied.
    - The function performs minimal checks to avoid leaking sensitive
      information about the existence of users or content.
    """
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content_item = CONTENT.get(cid)
    if not content_item:
        return "Access Denied"

    level_required = content_item.get("level")
    if _has_access(user, level_required):
        return content_item.get("title", "Untitled")
    else:
        return "Access Denied"