# -*- coding: utf-8 -*-
"""
Access‑control module.

This module implements a secure `retrieve_content` function that checks
whether a user is allowed to view a particular piece of content based on
their role and subscription level.

The module deliberately avoids any direct exposure to the underlying data
structures and performs defensive checks on all inputs.
"""

from __future__ import annotations

from typing import Dict, List

# ----------------------------------------------------------------------
# Sample data – in a real system these would be loaded from a database
# or an external service.
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, str]] = {
    # user_id : { "role": "...", "subscription_level": "..." }
    1: {"role": "admin", "subscription_level": "gold"},
    2: {"role": "user", "subscription_level": "silver"},
    3: {"role": "user", "subscription_level": "bronze"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    # content_id : { "title": "...", "required_level": "..." }
    101: {"title": "Advanced Topics in AI", "required_level": "gold"},
    102: {"title": "Intro to Python", "required_level": "bronze"},
    103: {"title": "Data Science Basics", "required_level": "silver"},
}

# Subscription hierarchy from lowest to highest.
SUBSCRIPTION_HIERARCHY: List[str] = ["bronze", "silver", "gold"]

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _level_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Levels not found are treated as lowest possible (index 0).
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError:
        # Unknown level – treat as lowest.
        return 0


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges; otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access content.
    contid : int
        The ID of the content requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Notes
    -----
    * Administrators (`role == "admin"`) bypass all checks.
    * Regular users may view content whose required level is **equal to or
      lower than** their own subscription level.
    * All lookups are performed defensively to avoid KeyError or
      accidental exposure of data.
    """
    # Defensive type checking – ensures we only operate on integers
    if not isinstance(usr_id, int) or not isinstance(contid, int):
        return "Access Denied"

    # Retrieve user data safely
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    # Admin users bypass checks
    if user.get("role") == "admin":
        content = CONTENT.get(contid)
        return content["title"] if content else "Access Denied"

    # Regular users – verify subscription level
    user_level = user.get("subscription_level")
    content = CONTENT.get(contid)
    if not content or not user_level:
        return "Access Denied"

    required_level = content.get("required_level")
    if not required_level:
        return "Access Denied"

    # Compare subscription levels
    if _level_index(user_level) >= _level_index(required_level):
        return content["title"]

    return "Access Denied"