# -*- coding: utf-8 -*-
"""
A simple access‑control module that demonstrates proper handling of user
subscription levels and role based permissions.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures – in a real system these would come from a DB
# --------------------------------------------------------------------------- #

USERS: dict[int, dict[str, str | int]] = {
    # usr_id : {role: 'admin'|'user', sub_level: subscription level}
    1: {"role": "admin", "sub_level": "premium"},
    2: {"role": "user", "sub_level": "basic"},
    3: {"role": "user", "sub_level": "standard"},
    4: {"role": "user", "sub_level": "premium"},
}

CONTENT: dict[int, dict[str, str]] = {
    # cont_id : {title: ..., required_level: subscription level}
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Standard Guide", "required_level": "standard"},
    103: {"title": "Premium Insights", "required_level": "premium"},
}

# Defines the order of subscription levels from lowest to highest
subscription_hierarchy = ["basic", "standard", "premium"]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _level_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Raises ValueError if the level is unknown.
    """
    try:
        return subscription_hierarchy.index(level)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Unknown subscription level: {level}") from exc


def _has_access(user_level: str, required_level: str) -> bool:
    """
    Determine whether a user with *user_level* can access content requiring
    *required_level*.  The check is inclusive: a user may access content of
    the same or lower tier.
    """
    return _level_index(user_level) >= _level_index(required_level)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges, otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting to access the content.
    contid : int
        Identifier of the content requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Notes
    -----
    - Administrators bypass all subscription checks.
    - If either the user or content does not exist, access is denied
      without leaking which entity was missing.
    """
    # Retrieve user and content in a single step to avoid timing attacks
    user = USERS.get(usr_id)
    content = CONTENT.get(contid)

    # If either lookup fails, deny access
    if user is None or content is None:
        return "Access Denied"

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must satisfy subscription level requirement
    user_level = user.get("sub_level")
    required_level = content.get("required_level")

    if not user_level or not required_level:
        return "Access Denied"

    if _has_access(user_level, required_level):
        return content["title"]

    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Demo: user 2 (basic) tries to access premium content
    print(retrieve_content(2, 103))  # Access Denied

    # Admin user
    print(retrieve_content(1, 103))  # Premium Insights

    # Valid access
    print(retrieve_content(3, 102))  # Standard Guide