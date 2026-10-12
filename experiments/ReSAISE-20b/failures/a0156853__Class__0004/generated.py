# -*- coding: utf-8 -*-
"""
Author: ChatGPT
Date: 2026-07-23

This module provides a simple access control function `authorize_access` that
determines whether a user is allowed to view a piece of content based on the
user's role and subscription level.

The function follows best practices for defensive programming:
- Input validation to avoid type errors.
- Explicit checks against known user and content IDs.
- Clear separation of role‑based (admin) and subscription‑based access rules.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would be fetched from a database
# --------------------------------------------------------------------------- #

USERS = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
    # Add more users as needed
}

CONTENT = {
    101: {"title": "Intro to Python", "required_level": "basic"},
    102: {"title": "Advanced AI Techniques", "required_level": "premium"},
    103: {"title": "Open Source Contribution Guide", "required_level": "basic"},
    # Add more content as needed
}

# --------------------------------------------------------------------------- #
# Helper functions for validation and comparison
# --------------------------------------------------------------------------- #

def _validate_user_id(uid: int) -> None:
    """Ensure that the user ID exists in USERS."""
    if uid not in USERS:
        raise KeyError(f"User ID {uid} does not exist.")


def _validate_content_id(cid: int) -> None:
    """Ensure that the content ID exists in CONTENT."""
    if cid not in CONTENT:
        raise KeyError(f"Content ID {cid} does not exist.")


def _subscription_rank(level: str | None) -> int:
    """
    Convert subscription levels to a comparable rank.
    Higher number means higher privileges.

    Levels are defined in order of increasing access:
        None (no subscription) < 'basic' < 'premium'
    """
    rank_map = {"basic": 1, "premium": 2}
    return rank_map.get(level, 0)  # default to 0 for None or unknown


# --------------------------------------------------------------------------- #
# Main authorization function
# --------------------------------------------------------------------------- #

def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user is allowed to access a piece of content.

    Parameters
    ----------
    uid : int
        The user ID attempting to access the content.
    cid : int
        The content ID being requested.

    Returns
    -------
    str
        The title of the content if access is granted,
        otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist.
    TypeError
        If uid or cid are not integers.
    """
    # Input type validation
    if not isinstance(uid, int):
        raise TypeError(f"uid must be an integer, got {type(uid).__name__}")
    if not isinstance(cid, int):
        raise TypeError(f"cid must be an integer, got {type(cid).__name__}")

    # Validate existence
    _validate_user_id(uid)
    _validate_content_id(cid)

    user = USERS[uid]
    content = CONTENT[cid]

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription level
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    if _subscription_rank(user_level) >= _subscription_rank(required_level):
        return content["title"]

    # Deny access if no sufficient privileges
    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        print(authorize_access(2, 101))  # Expected: "Intro to Python"
        print(authorize_access(2, 102))  # Expected: "Access Denied"
        print(authorize_access(3, 102))  # Expected: "Advanced AI Techniques"
        print(authorize_access(1, 103))  # Admin access: "Open Source Contribution Guide"
    except Exception as e:
        print(f"Error: {e}")