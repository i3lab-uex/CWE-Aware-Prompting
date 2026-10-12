# -*- coding: utf-8 -*-
"""
Utility module for content access control.

The `fetch_content` function checks whether a user is authorized to view
a particular piece of content.  Administrators are granted full access,
while regular users can only view content that matches their subscription
level.

CWE-284: Improper Access Control is mitigated by:
* Explicit role and level checks.
* Failure to expose internal data structures.
"""

from __future__ import annotations

# Sample user and content data.  In a real system these would be loaded
# from a database or external service.
USERS = {
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

CONTENT = {
    101: {"title": "Premium Article", "required_level": "gold"},
    102: {"title": "Silver Guide", "required_level": "silver"},
    103: {"title": "Bronze Tips", "required_level": "bronze"},
}

# Ordered list of subscription tiers for comparison.
SUBSCRIPTION_HIERARCHY = ["bronze", "silver", "gold"]


def _has_access(user: dict, content: dict) -> bool:
    """
    Determine if the user has permission to view the content.

    Parameters
    ----------
    user : dict
        User information containing 'role' and 'subscription'.
    content : dict
        Content information containing 'required_level'.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # Administrators bypass all checks
    if user.get("role") == "admin":
        return True

    # Non‑admins must have a subscription level that meets or exceeds
    # the required level for the content.
    user_level = user.get("subscription")
    required_level = content.get("required_level")

    try:
        return SUBSCRIPTION_HIERARCHY.index(user_level) >= SUBSCRIPTION_HIERARCHY.index(required_level)
    except ValueError:
        # Unknown subscription level – deny access
        return False


def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of a content item if the requesting user has access.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    cid : int
        Identifier of the desired content.

    Returns
    -------
    str
        Content title if access is granted, otherwise "Access Denied".

    Raises
    ------
    KeyError
        If the user_id or cid does not exist in their respective dictionaries.
    """
    # Retrieve user and content data; raise KeyError if not found
    user = USERS[user_id]
    content = CONTENT[cid]

    if _has_access(user, content):
        return content["title"]

    return "Access Denied"