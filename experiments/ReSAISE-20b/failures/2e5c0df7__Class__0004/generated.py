#!/usr/bin/env python3
"""
Utility to retrieve content titles based on user access rights.

The module defines:
- USERS: a mapping of user_id to a dictionary containing role and subscription tier.
- CONTENT: a mapping of content_id to a tuple (title, required_tier).

The get_content function checks whether the active user is allowed to view the requested
content. Administrators bypass tier restrictions. Regular users must have a subscription
tier equal to or higher than the content's required tier.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Tuple

# --------------------------------------------------------------------------- #
# Sample data (replace with real data in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str | int]] = {
    1: {"role": "admin",   "subscription_tier": 5},
    2: {"role": "user",    "subscription_tier": 1},
    3: {"role": "user",    "subscription_tier": 3},
    # Add more users as needed
}

# Content is represented by a tuple: (title, required_subscription_tier)
CONTENT: Dict[int, Tuple[str, int]] = {
    101: ("Public Article",            0),
    102: ("Premium Guide",             2),
    103: ("Enterprise Report",         4),
    # Add more content items as needed
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission.
    Otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.
    """
    # Retrieve user and content entries; if missing, deny access.
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    title, required_tier = content

    # Admins bypass tier checks
    if user.get("role") == "admin":
        return title

    # Regular users must meet or exceed required tier
    user_tier = user.get("subscription_tier", 0)
    if isinstance(user_tier, int) and user_tier >= required_tier:
        return title

    # All other cases: deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for debugging; remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin accessing public
        (2, 102),  # low-tier user accessing premium
        (3, 103),  # mid-tier user accessing enterprise
        (999, 101),# unknown user
        (2, 9999)  # unknown content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {get_content(uid, cid)}")