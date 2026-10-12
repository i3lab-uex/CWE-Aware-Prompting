# -*- coding: utf-8 -*-
"""
Content access control module.

This module defines a single function, `grant_access`, which checks whether
a user is allowed to view a piece of content based on their role and
subscription level.  The implementation follows best practices for
authorization checks, handling missing data gracefully, and guarding
against common security pitfalls such as missing authorization or
incomplete validation.
"""

from __future__ import annotations

# Example data structures.  In a real application these would come from
# a database or external service.
USERS = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT = {
    101: {"title": "Intro to Python", "required_level": "basic"},
    102: {"title": "Advanced Algorithms", "required_level": "premium"},
    103: {"title": "Admin Dashboard", "required_level": "admin"},
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine whether a user can access a specific content item.

    Parameters
    ----------
    user_id : int
        The identifier of the user attempting to access content.
    item_id : int
        The identifier of the content item.

    Returns
    -------
    str
        The title of the requested content if access is granted,
        otherwise the string 'Access Denied'.

    Notes
    -----
    * Admin users have unrestricted access to all content.
    * Regular users may only view items whose required subscription level
      matches or is lower than their own.  The hierarchy is:
          basic < premium < admin
    * All inputs are validated; missing users or items result in access
      denial rather than an exception.
    """
    # Retrieve user and content information safely.
    user = USERS.get(user_id)
    if not user:
        # Unknown user; deny access.
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        # Unknown item; deny access.
        return "Access Denied"

    role = user.get("role")
    sub_level_user = user.get("subscription_level")

    # Admin role bypasses subscription checks.
    if role == "admin":
        return content["title"]

    # Define subscription hierarchy for comparison.
    level_order = {"basic": 1, "premium": 2}

    # Validate subscription levels exist in the hierarchy.
    if sub_level_user not in level_order or content.get("required_level") not in level_order:
        return "Access Denied"

    # Check if user's subscription is sufficient.
    if level_order[sub_level_user] >= level_order[content["required_level"]]:
        return content["title"]

    # All other cases result in denial.
    return "Access Denied"


# Example usage (for testing purposes only; remove or guard under
# if __name__ == "__main__": in production code)
if __name__ == "__main__":
    tests = [
        (1, 101),  # admin accessing basic
        (2, 102),  # basic user trying premium content
        (3, 102),  # premium user accessing premium
        (4, 101),  # unknown user
        (2, 999),  # unknown content
    ]
    for uid, cid in tests:
        print(f"User {uid} accessing item {cid}: {grant_access(uid, cid)}")