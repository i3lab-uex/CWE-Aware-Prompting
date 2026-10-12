# -*- coding: utf-8 -*-
"""
Module providing access control for content viewing based on user subscription level.

The module defines a single public function `view_content` that checks whether
a user identified by `uid` is authorized to view a content item identified by
`cont_id`.  Administrators (role == 'admin') are granted unrestricted access.
Regular users may only view content whose required subscription level is
less than or equal to their own.

The function returns the title of the content if access is granted, otherwise
the string 'Access Denied'.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures – in a real system these would be loaded from a
# database or external service.  They are kept minimal for demonstration.
# --------------------------------------------------------------------------- #

USERS: dict[int, dict[str, str | int]] = {
    1: {"role": "admin", "subscription_level": 5},
    2: {"role": "user", "subscription_level": 3},
    3: {"role": "user", "subscription_level": 1},
}

CONTENT: dict[int, dict[str, str | int]] = {
    101: {"title": "Basic Guide", "required_level": 1},
    102: {"title": "Advanced Tutorial", "required_level": 3},
    103: {"title": "Pro Insights", "required_level": 5},
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(uid: int) -> dict[str, str | int] | None:
    """
    Safely retrieve a user record.

    Returns `None` if the user does not exist.
    """
    return USERS.get(uid)

def _get_content(cont_id: int) -> dict[str, str | int] | None:
    """
    Safely retrieve a content record.

    Returns `None` if the content does not exist.
    """
    return CONTENT.get(cont_id)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has permission to view it.

    Parameters
    ----------
    uid : int
        Identifier of the user attempting access.
    cont_id : int
        Identifier of the content item.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    * Administrators (`role == "admin"`) bypass subscription checks.
    * Regular users must have a `subscription_level` greater than or equal
      to the content's `required_level`.
    * If either the user or content record is missing, access is denied.
    """
    user = _get_user(uid)
    if not user:
        return "Access Denied"

    content = _get_content(cont_id)
    if not content:
        return "Access Denied"

    # Administrator bypass
    if user.get("role") == "admin":
        return content["title"]

    # Regular user access check
    try:
        user_level = int(user.get("subscription_level", 0))
        required_level = int(content.get("required_level", 0))
    except (ValueError, TypeError):
        # Malformed data – deny access to be safe
        return "Access Denied"

    if user_level >= required_level:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(view_content(1, 103))   # Admin access
#     print(view_content(2, 102))   # Allowed
#     print(view_content(3, 103))   # Denied