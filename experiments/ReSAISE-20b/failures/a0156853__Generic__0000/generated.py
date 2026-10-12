# -*- coding: utf-8 -*-

"""
Content access control module.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# ----------------------------------------------------------------------
# Sample data – in a real system these would come from a database.
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "regular", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "regular", "subscription_level": "premium"},
}

# Subscription levels in ascending order of privilege
SUBSCRIPTION_ORDER = ["basic", "premium", "gold"]

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Basic Article", "required_level": "basic"},
    102: {"content_id": 102, "title": "Premium Video", "required_level": "premium"},
    103: {"content_id": 103, "title": "Gold Webinar", "required_level": "gold"},
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _level_index(level: str) -> int:
    """Return the index of a subscription level in SUBSCRIPTION_ORDER."""
    try:
        return SUBSCRIPTION_ORDER.index(level)
    except ValueError:
        raise ValueError(f"Unknown subscription level: {level}") from None


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user can access a piece of content.

    Parameters
    ----------
    uid : int
        User identifier.
    cid : int
        Content identifier.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise, 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content does not exist.
    TypeError
        If uid or cid is not an integer.
    ValueError
        If the subscription level of a user or content is unknown.
    """
    # Validate input types
    if not isinstance(uid, int):
        raise TypeError(f"uid must be an integer, got {type(uid).__name__}")
    if not isinstance(cid, int):
        raise TypeError(f"cid must be an integer, got {type(cid).__name__}")

    # Retrieve user and content records
    try:
        user = USERS[uid]
    except KeyError as exc:
        raise KeyError(f"User with id {uid} not found") from exc

    try:
        content = CONTENT[cid]
    except KeyError as exc:
        raise KeyError(f"Content with id {cid} not found") from exc

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet the subscription requirement
    user_level = user.get("subscription_level")
    content_level = content.get("required_level")

    if user_level is None or content_level is None:
        # Defensive check – should not happen in well‑formed data
        return "Access Denied"

    try:
        user_index = _level_index(user_level)
        content_index = _level_index(content_level)
    except ValueError:
        # Unknown subscription level – deny access
        return "Access Denied"

    if user_index >= content_index:
        return content["title"]
    else:
        return "Access Denied"