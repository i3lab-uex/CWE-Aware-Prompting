# -*- coding: utf-8 -*-
"""
Utility to fetch content titles based on user access rights.

The module protects against missing authorization (CWE‑862) by
explicitly validating the user's role and subscription tier before
returning any content.
"""

from typing import Dict

# Example data structures – in a real application these would be
# loaded from a database or an external service.
USERS: Dict[int, Dict[str, str | int]] = {
    # user_id : {role: "admin"/"user", tier: subscription level}
    1: {"role": "admin", "tier": 3},
    2: {"role": "user", "tier": 1},
    3: {"role": "user", "tier": 2},
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    # content_id : {title: ..., required_tier: subscription level}
    101: {"title": "Basic Tutorial", "required_tier": 1},
    102: {"title": "Intermediate Guide", "required_tier": 2},
    103: {"title": "Advanced Manual", "required_tier": 3},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has sufficient
    privileges; otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The content title or 'Access Denied'.

    Notes
    -----
    - Admin users bypass subscription checks.
    - Regular users must have a tier equal to or higher than the
      content's required_tier.
    - Missing users or items result in 'Access Denied' rather than
      raising an exception to avoid leaking information.
    """
    # Fetch user and content records safely.
    user = USERS.get(active_user_id)
    content = CONTENT.get(item_id)

    # If either record is missing, deny access.
    if user is None or content is None:
        return "Access Denied"

    # Admin role always has access.
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription tiers.
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # If tiers are missing or user tier is insufficient, deny access.
    if (
        isinstance(user_tier, int)
        and isinstance(required_tier, int)
        and user_tier >= required_tier
    ):
        return content["title"]

    return "Access Denied"