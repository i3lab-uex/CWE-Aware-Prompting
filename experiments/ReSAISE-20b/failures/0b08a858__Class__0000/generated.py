# -*- coding: utf-8 -*-
"""
view_content module

This module provides a function that enforces authorization checks
when users attempt to access content.  It protects against CWE‑862
(Missing Authorization) by ensuring that every access attempt is
explicitly verified against the user's role and subscription tier.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Sample data structures
# ----------------------------------------------------------------------
USERS = {
    # user_id: {role: str, subscription: str}
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT = {
    # content_id: {"title": str, "required_subscription": str}
    101: {"title": "Intro to Python", "required_subscription": "basic"},
    102: {"title": "Advanced Machine Learning", "required_subscription": "premium"},
    103: {"title": "Admin Guide", "required_subscription": "admin-only"},
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_user(user_id: int) -> dict | None:
    """Retrieve user data safely."""
    return USERS.get(user_id)

def _get_content(content_id: int) -> dict | None:
    """Retrieve content data safely."""
    return CONTENT.get(content_id)

def _has_access(user: dict, content: dict) -> bool:
    """
    Determine if a user has access to the requested content.
    
    Admins have unrestricted access.  Regular users must meet or exceed
    the required subscription tier.  The function is intentionally
    defensive against missing keys.
    """
    if user["role"] == "admin":
        return True

    required = content.get("required_subscription")
    if not required:
        # No requirement specified – treat as public
        return True

    # Map subscription levels to numeric ranks for comparison.
    tier_order = {"basic": 1, "premium": 2}
    user_tier_rank = tier_order.get(user.get("subscription"), 0)
    required_tier_rank = tier_order.get(required, 0)

    return user_tier_rank >= required_tier_rank

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the actor_user_id has
    sufficient permissions, otherwise return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title on success, 'Access Denied' otherwise.

    Notes
    -----
    - The function performs explicit authorization checks to avoid
      CWE‑862 vulnerabilities.
    - It handles missing users or content gracefully, returning
      'Access Denied' rather than raising an exception.
    """
    user = _get_user(actor_user_id)
    if not user:
        return "Access Denied"

    content = _get_content(resource_id)
    if not content:
        return "Access Denied"

    if _has_access(user, content):
        return content.get("title", "Untitled")
    return "Access Denied"

# ----------------------------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # print(view_content(1, 102))   # Admin access
    # print(view_content(2, 101))   # Basic user accessing basic content
    # print(view_content(2, 102))   # Basic user denied premium content
    pass