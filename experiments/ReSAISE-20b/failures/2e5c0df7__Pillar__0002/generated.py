# -*- coding: utf-8 -*-
"""
Utility for controlled content access.

The module defines a single function `get_content` which checks whether
a user is allowed to view a particular piece of content based on their role
and subscription tier.  The function is intentionally defensive:
it never raises unhandled exceptions for missing data and it uses
exact membership checks to avoid common access‑control pitfalls
(CWE‑284).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data structures – replace these with real data sources in production
# --------------------------------------------------------------------------- #

USERS: dict[int, dict[str, str | int]] = {
    # user_id : {role: 'admin' or 'user', tier: subscription level}
    1: {"role": "admin", "tier": "gold"},
    2: {"role": "user", "tier": "silver"},
    3: {"role": "user", "tier": "bronze"},
}

CONTENT: dict[int, dict[str, str | int]] = {
    # content_id : {title: ..., required_tier: subscription level}
    101: {"title": "Premium Article", "required_tier": "gold"},
    102: {"title": "Silver Guide", "required_tier": "silver"},
    103: {"title": "Bronze Basics", "required_tier": "bronze"},
}

# --------------------------------------------------------------------------- #
# Helper: tier hierarchy
# --------------------------------------------------------------------------- #

TIER_ORDER = {"bronze": 1, "silver": 2, "gold": 3}

def _has_access(user_tier: str | int, required_tier: str | int) -> bool:
    """
    Determine whether a user tier grants access to content requiring
    a certain tier.

    Parameters:
        user_tier (str | int): The user's subscription level.
        required_tier (str | int): The tier required for the content.

    Returns:
        bool: True if access is allowed, False otherwise.
    """
    try:
        user_rank = TIER_ORDER[str(user_tier).lower()]
        required_rank = TIER_ORDER[str(required_tier).lower()]
    except KeyError:
        # Unknown tier – deny access
        return False

    return user_rank >= required_rank


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user is authorized to view it.

    The function enforces access control as follows:
        * Administrators (role == 'admin') may view any content.
        * Regular users must have a subscription tier equal to or higher
          than the tier required by the content.

    Parameters:
        active_user_id (int): Identifier of the user attempting access.
        item_id (int): Identifier of the requested content.

    Returns:
        str: The content title if authorized, otherwise 'Access Denied'.
    """
    # Fetch user and content data safely
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # Admins bypass tier checks
    if user.get("role") == "admin":
        return content.get("title", "Access Denied")

    # Regular users must satisfy tier requirement
    if _has_access(user.get("tier"), content.get("required_tier")):
        return content.get("title", "Access Denied")

    # All other cases – deny access
    return "Access Denied"