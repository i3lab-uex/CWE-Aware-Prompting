# -*- coding: utf-8 -*-
"""
Content access control module.

The function `fetch_content` performs an authorization check before
returning the requested content title.  Administrators are granted full
access; regular users may only view content that matches or is lower than
their subscription level.

The module includes defensive programming practices to mitigate
CWE‑862 (Missing Authorization) and other common security issues.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real data sources in production)
# --------------------------------------------------------------------------- #

# Mapping of user IDs to their role and subscription level.
USERS = {
    1: {"role": "admin",      "subscription_level": "premium"},
    2: {"role": "user",       "subscription_level": "basic"},
    3: {"role": "user",       "subscription_level": "standard"},
    4: {"role": "guest",      "subscription_level": None},   # No subscription
}

# Mapping of content IDs to the required subscription level and title.
CONTENT = {
    101: {"required_level": "basic",    "title": "Intro to Python"},
    102: {"required_level": "standard", "title": "Advanced Data Structures"},
    103: {"required_level": "premium",  "title": "Machine Learning Mastery"},
}

# Ordered subscription levels for comparison (lowest to highest)
SUBSCRIPTION_ORDER = ["basic", "standard", "premium"]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user_info(user_id: int) -> dict | None:
    """Retrieve user information, returning None if the user does not exist."""
    return USERS.get(user_id)

def _get_content_info(cid: int) -> dict | None:
    """Retrieve content information, returning None if the content does not exist."""
    return CONTENT.get(cid)

def _has_access(user_info: dict, content_info: dict) -> bool:
    """
    Determine if a user has access to the requested content.

    Parameters
    ----------
    user_info : dict
        Dictionary containing at least 'role' and 'subscription_level'.
    content_info : dict
        Dictionary containing at least 'required_level'.

    Returns
    -------
    bool
        True if access is allowed, False otherwise.
    """
    # Administrators bypass all checks
    if user_info.get("role") == "admin":
        return True

    # Regular users must have a subscription level
    user_level = user_info.get("subscription_level")
    required_level = content_info.get("required_level")

    if not user_level or not required_level:
        return False

    # Compare levels using the predefined order
    try:
        user_index = SUBSCRIPTION_ORDER.index(user_level)
        required_index = SUBSCRIPTION_ORDER.index(required_level)
    except ValueError:
        # Unknown level names – deny access
        return False

    # User's level must be equal or higher than required
    return user_index >= required_index

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access content.
    cid : int
        The content ID being requested.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise
        'Access Denied'.

    Raises
    ------
    TypeError
        If arguments are not integers.
    """
    # Input validation – guard against type confusion attacks
    if not isinstance(user_id, int):
        raise TypeError("user_id must be an integer")
    if not isinstance(cid, int):
        raise TypeError("cid must be an integer")

    user_info = _get_user_info(user_id)
    if not user_info:
        return "Access Denied"

    content_info = _get_content_info(cid)
    if not content_info:
        return "Access Denied"

    if _has_access(user_info, content_info):
        # Safely return the title; avoid exposing internal keys
        return content_info["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(fetch_content(1, 103))  # Admin: should succeed
    print(fetch_content(2, 101))  # Basic user: should succeed
    print(fetch_content(3, 103))  # Standard user: should fail