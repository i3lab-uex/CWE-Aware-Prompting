# -*- coding: utf-8 -*-
"""
Utility module for content access control.

The `get_content` function determines whether a user is allowed to view a
particular piece of content based on their role and subscription tier.
"""

from __future__ import annotations

from typing import Dict, Any

# Example data structures – in real code these would come from a database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "member", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "member", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Premium Article", "required_tier": "premium"},
    102: {"content_id": 102, "title": "Basic Article",   "required_tier": "basic"},
    103: {"content_id": 103, "title": "General Article", "required_tier": None},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access the content.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title if access is granted, otherwise "Access Denied".

    Notes
    -----
    * Administrators (role == 'admin') may access any content.
    * Regular users must have a subscription tier that matches or exceeds
      the required tier of the content.  The tier hierarchy is:
        'basic' < 'premium'.
    * If either the user or the content does not exist, access is denied.
    """
    # Defensive lookup – avoid KeyError
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Determine tier hierarchy
    tier_order = {"basic": 1, "premium": 2}
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # If the content has no tier requirement, it's public
    if required_tier is None:
        return content["title"]

    # Validate tiers exist in the hierarchy
    if user_tier not in tier_order or required_tier not in tier_order:
        return "Access Denied"

    # Grant access if user's tier level is >= required tier level
    if tier_order[user_tier] >= tier_order[required_tier]:
        return content["title"]

    return "Access Denied"


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(get_content(1, 101))  # Admin: should see title
#     print(get_content(2, 101))  # Basic user trying premium content: denied
#     print(get_content(3, 102))  # Premium user accessing basic content: allowed