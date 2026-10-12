# -*- coding: utf-8 -*-

"""
Utility module for content access control.

This module provides a single public function `get_content` that determines
whether a user is allowed to view a particular piece of content based on
their role and subscription tier.  Administrators (role == 'admin') are
unconditionally granted access, while regular users may only view content
whose required tier is less than or equal to their own subscription tier.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data structures.  In a real application these would come from a
# database or external service.
# --------------------------------------------------------------------------- #

USERS: dict[int, dict[str, str | int]] = {
    # user_id : {role: 'admin'|'user', tier: int}
    1: {"role": "admin", "tier": 0},
    2: {"role": "user",  "tier": 1},
    3: {"role": "user",  "tier": 2},
    4: {"role": "user",  "tier": 3},
}

CONTENT: dict[int, dict[str, str | int]] = {
    # content_id : {title: str, required_tier: int}
    101: {"title": "Intro to Python",          "required_tier": 1},
    102: {"title": "Advanced Machine Learning","required_tier": 2},
    103: {"title": "Enterprise Security",      "required_tier": 3},
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content ID does not exist.
    """
    # Retrieve user and content records.  KeyError will propagate if missing,
    # signalling a programming error rather than silently denying access.
    user = USERS[active_user_id]
    content_item = CONTENT[item_id]

    # Admins bypass all checks
    if user["role"] == "admin":
        return content_item["title"]

    # Regular users must have a tier >= required_tier
    if user.get("tier", 0) >= content_item["required_tier"]:
        return content_item["title"]

    # All other cases are denied
    return "Access Denied"


# --------------------------------------------------------------------------- #
# If run as a script, demonstrate usage
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin accessing any content
        (2, 101),  # tier 1 user accessing tier 1 content
        (2, 102),  # tier 1 user accessing tier 2 content
        (3, 102),  # tier 2 user accessing tier 2 content
        (4, 103),  # tier 3 user accessing tier 3 content
    ]

    for uid, cid in test_cases:
        try:
            result = get_content(uid, cid)
            print(f"User {uid} accessing content {cid}: {result}")
        except KeyError as exc:
            print(f"Invalid ID(s) for user {uid} or content {cid}: {exc}")