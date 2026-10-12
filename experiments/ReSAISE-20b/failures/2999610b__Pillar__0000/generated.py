# -*- coding: utf-8 -*-

"""
Module: access_control

Provides a single function `retrieve_content` that checks whether a user
has permission to view a particular piece of content based on their role
and subscription level.

Security considerations:
* The function validates input types to prevent type‑based attacks.
* Administrator users bypass subscription checks entirely.
* All comparisons use the defined hierarchy; no direct string comparison
  is performed to avoid case‑sensitive or partial matches.
* Invalid user IDs or content IDs raise a ValueError to avoid silent
  failures that could leak information.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Data definitions
# --------------------------------------------------------------------------- #

USERS = {
    # user_id: {"role": str, "subscription": str}
    1: {"role": "admin",   "subscription": "premium"},
    2: {"role": "user",    "subscription": "basic"},
    3: {"role": "user",    "subscription": "premium"},
    4: {"role": "user",    "subscription": "gold"},
}

CONTENT = {
    # content_id: {"title": str, "required_subscription": str}
    101: {"title": "Public Guide",          "required_subscription": "basic"},
    102: {"title": "Premium Tutorial",     "required_subscription": "premium"},
    103: {"title": "Gold Insights",        "required_subscription": "gold"},
}

# Lower value = lower tier
subscription_hierarchy = ["basic", "premium", "gold"]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_int(value: int, name: str) -> None:
    """
    Ensure the provided value is an integer.
    Raises TypeError if not.
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")


def _get_user_info(user_id: int) -> dict:
    """Retrieve user info, raising ValueError if not found."""
    try:
        return USERS[user_id]
    except KeyError as exc:
        raise ValueError(f"Unknown user ID: {user_id}") from exc


def _get_content_info(content_id: int) -> dict:
    """Retrieve content info, raising ValueError if not found."""
    try:
        return CONTENT[content_id]
    except KeyError as exc:
        raise ValueError(f"Unknown content ID: {content_id}") from exc


def _subscription_index(level: str) -> int:
    """Return the index of a subscription level in the hierarchy."""
    try:
        return subscription_hierarchy.index(level)
    except ValueError as exc:
        raise ValueError(f"Invalid subscription level: {level}") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    permissions, otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting to access content.
    contid : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The title of the content or 'Access Denied'.

    Raises
    ------
    TypeError
        If arguments are not integers.
    ValueError
        If user ID or content ID does not exist, or if subscription levels are invalid.
    """
    # Validate input types
    _validate_int(usr_id, "usr_id")
    _validate_int(contid, "contid")

    # Fetch user and content metadata
    user = _get_user_info(usr_id)
    content = _get_content_info(contid)

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Compare subscription levels
    user_level = user.get("subscription")
    required_level = content.get("required_subscription")

    # If any level is missing or invalid, deny access
    if user_level is None or required_level is None:
        return "Access Denied"

    # Ensure levels exist in the hierarchy
    try:
        user_idx = _subscription_index(user_level)
        required_idx = _subscription_index(required_level)
    except ValueError:
        return "Access Denied"

    # Grant access if user level is equal or higher
    if user_idx >= required_idx:
        return content["title"]

    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(retrieve_content(2, 101))  # Public Guide
#     print(retrieve_content(2, 102))  # Access Denied
#     print(retrieve_content(1, 103))  # Gold Insights (admin)