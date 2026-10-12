#!/usr/bin/env python3
"""
Access control module for content viewing.

This module implements the `view_content` function which enforces
subscription‑based access control.  Administrators can view all content,
while regular users may only view content that matches their
subscription tier.

The implementation follows best practices to mitigate CWE‑284
(Improper Access Control).  It validates input types, checks for the
existence of users and content, and uses strict equality comparisons.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Sample data – in a real application these would come from a database
# ----------------------------------------------------------------------
USERS: dict[int, dict[str, str | int]] = {
    1: {"role": "admin", "subscription_tier": "gold"},
    2: {"role": "user", "subscription_tier": "silver"},
    3: {"role": "user", "subscription_tier": "bronze"},
}

CONTENT: dict[int, dict[str, str]] = {
    101: {"title": "Advanced Python", "required_tier": "gold"},
    102: {"title": "Intro to Programming", "required_tier": "bronze"},
    103: {"title": "Data Science Basics", "required_tier": "silver"},
}

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content being accessed.

    Returns
    -------
    str
        The content title if access is granted, or 'Access Denied'.

    Notes
    -----
    - Administrators have unrestricted access.
    - Regular users must meet or exceed the required subscription tier.
      The tier hierarchy is defined in _TIER_HIERARCHY.

    Raises
    ------
    TypeError
        If arguments are not integers.
    """
    # Validate input types to avoid accidental injection of non‑int values
    if not isinstance(actor_user_id, int) or not isinstance(resource_id, int):
        raise TypeError("actor_user_id and resource_id must be integers")

    # Retrieve user and content data
    user = USERS.get(actor_user_id)
    content = CONTENT.get(resource_id)

    # If either the user or the content does not exist, deny access
    if user is None or content is None:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must satisfy the subscription requirement
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    if _has_access(user_tier, required_tier):
        return content["title"]

    # Default denial
    return "Access Denied"

# ----------------------------------------------------------------------
# Helper functions & constants
# ----------------------------------------------------------------------
_TIER_HIERARCHY = {"bronze": 1, "silver": 2, "gold": 3}

def _has_access(user_tier: str | None, required_tier: str | None) -> bool:
    """
    Determine if a user tier meets or exceeds the required tier.

    Parameters
    ----------
    user_tier : str | None
        The user's subscription tier.
    required_tier : str | None
        The content's required subscription tier.

    Returns
    -------
    bool
        True if the user has sufficient privileges, False otherwise.
    """
    if user_tier is None or required_tier is None:
        return False
    return _TIER_HIERARCHY.get(user_tier, 0) >= _TIER_HIERARCHY.get(required_tier, 0)

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     print(view_content(1, 101))  # Admin access
#     print(view_content(2, 103))  # Silver user accessing silver content
#     print(view_content(3, 102))  # Bronze user accessing bronze content
#     print(view_content(2, 101))  # Silver user denied gold content