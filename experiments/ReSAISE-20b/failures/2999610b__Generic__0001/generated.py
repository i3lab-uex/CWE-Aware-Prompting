#!/usr/bin/env python3
"""
Utility to retrieve content titles based on user subscription levels.

The module defines:
- USERS: mapping from user IDs to a dict containing their role and subscription level.
- CONTENT: mapping from content IDs to a dict containing the title and required subscription level.
- SUBSCRIPTION_HIERARCHY: list defining the order of subscription levels from lowest to highest.

The `retrieve_content` function checks whether a user has permission to access a given content item.
Administrators have unrestricted access; regular users can only view content at or below their subscription level.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription_level: str}
    1: {"role": "admin",   "subscription_level": "platinum"},
    2: {"role": "user",    "subscription_level": "gold"},
    3: {"role": "user",    "subscription_level": "silver"},
    4: {"role": "guest",   "subscription_level": "basic"},   # unknown role
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_subscription_level: str}
    101: {"title": "Introduction to Python",          "required_subscription_level": "basic"},
    102: {"title": "Advanced Machine Learning",       "required_subscription_level": "gold"},
    103: {"title": "Quantum Computing Overview",      "required_subscription_level": "platinum"},
    104: {"title": "Open Source Contributions Guide", "required_subscription_level": "silver"},
}

# Subscription levels from lowest to highest
SUBSCRIPTION_HIERARCHY = ["basic", "silver", "gold", "platinum"]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _subscription_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Raises ValueError if the level is not found.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


def _has_access(user_level: str, content_level: str) -> bool:
    """
    Determine if a user with `user_level` can access content requiring `content_level`.
    """
    return _subscription_index(user_level) >= _subscription_index(content_level)


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Retrieve the title of a content item if the user has permission.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting to access the content.
    contid : int
        Identifier of the desired content item.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist.
    ValueError
        If an unknown subscription level is encountered.
    """
    # Validate existence of user and content entries
    try:
        user = USERS[usr_id]
    except KeyError as exc:
        raise KeyError(f"User ID {usr_id} not found") from exc

    try:
        content = CONTENT[contid]
    except KeyError as exc:
        raise KeyError(f"Content ID {contid} not found") from exc

    # Administrators bypass all checks
    if user.get("role", "").lower() == "admin":
        return content["title"]

    # For regular users, check subscription level
    user_level = user.get("subscription_level", "").lower()
    required_level = content.get("required_subscription_level", "").lower()

    if not user_level or not required_level:
        # Missing subscription data – deny access as a safety measure
        return "Access Denied"

    if _has_access(user_level, required_level):
        return content["title"]

    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin
        (2, 102),  # gold user accessing gold content
        (3, 103),  # silver user trying platinum content
        (4, 104),  # guest with basic level accessing silver content
    ]

    for uid, cid in test_cases:
        try:
            print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")
        except Exception as e:
            print(f"Error for user {uid} and content {cid}: {e}")