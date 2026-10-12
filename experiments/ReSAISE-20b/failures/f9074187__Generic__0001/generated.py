# SPDX-License-Identifier: MIT

"""
Content access control module.

Defines a `grant_access` function that checks whether a user has permission
to view a piece of content based on their role and subscription level.
"""

from __future__ import annotations

# Example data structures. In a real application these would be fetched from
# a database or external service.
USERS = {
    # user_id: {role: str, subscription_level: str}
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT = {
    # content_id: {"title": str, "required_level": str}
    101: {"title": "Advanced Python Guide", "required_level": "premium"},
    102: {"title": "Intro to Programming", "required_level": "basic"},
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine whether a user is allowed to access the requested content.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access the content.
    item_id : int
        The ID of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise, 'Access Denied'.

    Notes
    -----
    - Admin users bypass all subscription checks.
    - Regular users may only access content whose required level is less
      than or equal to their own subscription level.
    - The function gracefully handles missing user or content IDs by
      returning 'Access Denied'.
    """
    # Basic type validation for security.
    if not isinstance(user_id, int) or not isinstance(item_id, int):
        raise TypeError("user_id and item_id must be integers")

    user = USERS.get(user_id)
    content = CONTENT.get(item_id)

    if user is None or content is None:
        return "Access Denied"

    # Admins have full access.
    if user.get("role") == "admin":
        return content["title"]

    # Define a simple hierarchy for subscription levels.
    level_order = {"basic": 1, "premium": 2}

    user_level = level_order.get(user.get("subscription_level", "").lower())
    required_level = level_order.get(content.get("required_level", "").lower())

    if user_level is None or required_level is None:
        return "Access Denied"

    # Grant access if the user's level meets or exceeds the required level.
    return content["title"] if user_level >= required_level else "Access Denied"