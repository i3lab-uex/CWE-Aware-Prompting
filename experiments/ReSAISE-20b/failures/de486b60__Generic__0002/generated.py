#!/usr/bin/env python3
"""
Utility for content access control.

The module exposes a single function, `view_content`, which determines
whether a user is allowed to view a particular piece of content based on
their role and subscription level.

Author: ChatGPT
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real data in production)
# --------------------------------------------------------------------------- #

# Mapping of user_id -> {"role": str, "subscription_level": int}
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": 3},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
}

# Mapping of content_id -> {"title": str, "required_level": int}
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Public Article", "required_level": 0},
    102: {"title": "Basic Video", "required_level": 1},
    103: {"title": "Premium Podcast", "required_level": 2},
    104: {"title": "Admin Guide", "required_level": 3},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has permission to view it.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to access the content.
    cont_id : int
        The ID of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    * Administrators (`role == "admin"`) have unrestricted access.
    * Regular users may view content whose `required_level` is less than
      or equal to their own subscription level.
    * If either the user ID or content ID does not exist in the
      respective dictionaries, access is denied.
    """
    # Fetch user and content safely; if missing return denial
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription level
    user_level = user.get("subscription_level", 0)
    required_level = content.get("required_level", 0)

    if user_level >= required_level:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 104),  # Admin accessing admin guide
        (2, 102),  # User level 1 accessing required_level 1
        (3, 103),  # User level 2 accessing required_level 2
        (2, 103),  # User level 1 attempting premium content
        (4, 101),  # Unknown user
        (2, 999),  # Unknown content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {view_content(uid, cid)}")