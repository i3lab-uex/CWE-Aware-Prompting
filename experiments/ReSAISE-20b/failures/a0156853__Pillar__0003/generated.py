#!/usr/bin/env python3
"""
Secure content access control based on user role and subscription level.

Author: ChatGPT
"""

from typing import Dict

# Example data structures. In production these would be fetched from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Advanced Guide", "required_level": "premium"},
    103: {"title": "Admin Manual", "required_level": "admin"},
}

# Define the hierarchy of subscription levels.
SUBSCRIPTION_RANK = {
    "basic": 1,
    "premium": 2,
    # Admins are handled separately by role.
}


def _validate_int(value, name: str) -> None:
    """Raise a ValueError if the value is not an integer."""
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an integer, got {type(value).__name__}")


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user can access the requested content.

    Parameters
    ----------
    uid : int
        User identifier.
    cid : int
        Content identifier.

    Returns
    -------
    str
        The content title if access is granted, otherwise 'Access Denied'.
    """
    # Basic type validation to guard against injection of non‑int values.
    _validate_int(uid, "uid")
    _validate_int(cid, "cid")

    # Retrieve user and content records. Use .get() to avoid KeyError.
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access.
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription level.
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If the content requires admin level, deny regular users.
    if required_level == "admin":
        return "Access Denied"

    # Compare subscription ranks.
    user_rank = SUBSCRIPTION_RANK.get(user_level, 0)
    required_rank = SUBSCRIPTION_RANK.get(required_level, 0)

    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"


# Example usage (for testing purposes)
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin accessing basic
        (2, 102),  # basic user accessing premium
        (3, 102),  # premium user accessing premium
        (2, 103),  # basic user accessing admin content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {authorize_access(uid, cid)}")