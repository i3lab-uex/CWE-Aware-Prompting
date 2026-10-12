# -*- coding: utf-8 -*-
"""
Utility to fetch content based on user role and subscription level.

The module defines two dictionaries:
- USERS: maps user_id to a dict containing the user's role and subscription level.
- CONTENT: maps content_id to a dict containing the required subscription level and title.

The main function `fetch_content` checks whether a user has sufficient privileges to access
the requested content and returns the title if allowed, otherwise it returns "Access Denied".
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Data definitions (example data – replace with real data in production)
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
    # ... additional users
}

# Subscription hierarchy: lower index means less privileged
SUBSCRIPTION_HIERARCHY = ["basic", "standard", "premium"]

CONTENT = {
    101: {"title": "Introduction to Python", "required_subscription": "basic"},
    102: {"title": "Advanced Data Structures", "required_subscription": "standard"},
    103: {"title": "Machine Learning Mastery", "required_subscription": "premium"},
    # ... additional content items
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _subscription_index(sub: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Lower indices represent lower privileges.

    Raises:
        ValueError: if the subscription level is unknown.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(sub.lower())
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {sub}") from exc


def _has_access(user_info: dict, content_info: dict) -> bool:
    """
    Determine if a user has access to a piece of content.

    Admins have full access. Regular users must have a subscription level
    that is equal to or higher than the content's required level.
    """
    if user_info.get("role") == "admin":
        return True

    user_sub = user_info.get("subscription")
    content_req = content_info.get("required_subscription")

    if not user_sub or not content_req:
        return False

    try:
        return _subscription_index(user_sub) >= _subscription_index(content_req)
    except ValueError:
        # Unknown subscription levels result in denial
        return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the content with id `cid` if the user identified by
    `user_id` has sufficient privileges, otherwise return "Access Denied".

    Parameters:
        user_id (int): The ID of the requesting user.
        cid (int):   The content ID being requested.

    Returns:
        str: Title of the content or "Access Denied".

    Security Notes:
        - The function does not expose whether a user ID or content ID is invalid.
          It simply returns "Access Denied" for any failure case, preventing
          enumeration attacks.
        - All data is treated as immutable during the function call to avoid
          accidental modifications.
    """
    # Retrieve user and content info; default to empty dicts if not found
    user_info = USERS.get(user_id, {})
    content_info = CONTENT.get(cid)

    if not content_info:
        # Unknown content ID – deny access without revealing specifics
        return "Access Denied"

    if _has_access(user_info, content_info):
        # Safely return the title; strip any leading/trailing whitespace
        return content_info.get("title", "").strip()
    else:
        return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(fetch_content(1, 101))  # Admin – should return title
    print(fetch_content(2, 102))  # Basic user trying to access standard content – denied
    print(fetch_content(3, 103))  # Premium user accessing premium content – allowed