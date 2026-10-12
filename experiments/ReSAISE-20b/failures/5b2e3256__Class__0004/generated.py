# -*- coding: utf-8 -*-
"""
Secure content access implementation.

This module defines a simple authorization routine that checks whether
a user has permission to view a piece of content based on their role
and subscription level.  The implementation protects against the
CWE-862 vulnerability (Missing Authorization) by performing a
mandatory authorization check for every access request.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures
# --------------------------------------------------------------------------- #

# USERS maps user_id -> dict with 'role' and 'subscription'.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin",   "subscription": "premium"},
    2: {"role": "user",    "subscription": "basic"},
    3: {"role": "user",    "subscription": "premium"},
}

# CONTENT maps content_id -> dict with 'title' and required subscription level.
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Intro to Python",      "level": "basic"},
    102: {"title": "Advanced Algorithms",  "level": "premium"},
    103: {"title": "Admin Guide",          "level": "admin"},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has
    sufficient permissions; otherwise return 'Access Denied'.

    Parameters:
        user_id (int): The ID of the requesting user.
        cid     (int): The content ID being requested.

    Returns:
        str: Content title or 'Access Denied'.

    Raises:
        KeyError: If user_id or cid is not found in the respective dictionaries.
    """
    # Retrieve user and content records; raise KeyError if missing
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} does not exist.") from exc

    try:
        content = CONTENT[cid]
    except KeyError as exc:
        raise KeyError(f"Content ID {cid} does not exist.") from exc

    # Administrator bypasses subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, verify subscription level
    required_level = content.get("level")
    user_level = user.get("subscription")

    # Define a simple hierarchy for comparison
    levels = {"basic": 1, "premium": 2, "admin": 3}

    # If the required level is not defined or unknown, deny access
    if required_level not in levels:
        return "Access Denied"

    # Compare numeric values; user must meet or exceed required level
    if levels.get(user_level, 0) >= levels[required_level]:
        return content["title"]

    # If all checks fail, deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Should succeed: admin accessing any content
    print(fetch_content(1, 101))  # Intro to Python

    # Should succeed: premium user accessing premium content
    print(fetch_content(3, 102))  # Advanced Algorithms

    # Should fail: basic user accessing premium content
    print(fetch_content(2, 102))  # Access Denied

    # Should fail: missing content
    try:
        print(fetch_content(2, 999))
    except KeyError as e:
        print(e)