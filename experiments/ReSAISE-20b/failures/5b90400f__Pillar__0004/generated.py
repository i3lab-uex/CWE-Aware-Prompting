# -*- coding: utf-8 -*-
"""
Access control module.

This module defines a single function `access_content` that enforces
subscription-based access to content.  It follows the principle of least
privilege and protects against CWE-284: Improper Access Control.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data structures.  In a real application these would be replaced by
# database queries or external services.
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT = {
    101: {"title": "Premium Article", "required_subscription": "premium"},
    102: {"title": "Basic Guide", "required_subscription": "basic"},
    103: {"title": "Admin Manual", "required_subscription": "admin"},  # special case
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> dict | None:
    """Return user data or None if not found."""
    return USERS.get(user_id)

def _get_content(content_id: int) -> dict | None:
    """Return content data or None if not found."""
    return CONTENT.get(content_id)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def access_content(current_user_id: int, content_id: int) -> dict | str:
    """
    Return the requested content if the user is authorized, otherwise
    return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access content.
    content_id : int
        The identifier of the requested content.

    Returns
    -------
    dict | str
        Content data if authorized, otherwise 'Access Denied'.

    Notes
    -----
    * Admins have unrestricted access.
    * Regular users must meet or exceed the required subscription level.
      The hierarchy is: 'basic' < 'premium'.
    * Content that requires role 'admin' can only be accessed by admins.
    """
    # Retrieve user and content; fail fast if either is missing
    user = _get_user(current_user_id)
    if not user:
        return "Access Denied"

    content = _get_content(content_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content

    # Content that explicitly requires admin role
    if content.get("required_subscription") == "admin":
        return "Access Denied"

    # Map subscription levels to numeric values for comparison
    sub_levels = {"basic": 1, "premium": 2}
    user_level = sub_levels.get(user.get("subscription"), 0)
    content_level = sub_levels.get(content.get("required_subscription"), 0)

    if user_level >= content_level:
        return content

    # Default deny
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (commented out; remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(access_content(1, 101))  # Admin accessing premium content
#     print(access_content(2, 101))  # Basic user trying to access premium content
#     print(access_content(3, 102))  # Premium user accessing basic content