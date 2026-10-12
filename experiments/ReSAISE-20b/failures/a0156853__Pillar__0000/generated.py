# -*- coding: utf-8 -*-
"""
Secure access control for content based on user role and subscription level.
"""

from typing import Dict, Any

# Example data structures – in a real application these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin",   "subscription_level": "premium"},
    2: {"user_id": 2, "role": "user",    "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user",    "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Tutorial",      "required_level": "basic"},
    102: {"title": "Premium Insights",    "required_level": "premium"},
    103: {"title": "Admin Dashboard",     "required_level": "admin"},
}

# Define a clear hierarchy for subscription levels.
SUBSCRIPTION_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    # 'admin' is a role, not a subscription level
}

def _level_value(level: str) -> int:
    """
    Convert a subscription level string to an integer value.
    Non‑existent levels are treated as 0 (no access).
    """
    return SUBSCRIPTION_HIERARCHY.get(level.lower(), 0)

def authorize_access(uid: int, cid: int) -> str:
    """
    Return the title of the content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        User identifier.
    cid : int
        Content identifier.

    Returns
    -------
    str
        Title of the content or 'Access Denied'.
    """
    # Retrieve user and content data; fail gracefully if not found.
    user = USERS.get(uid)
    content = CONTENT.get(cid)

    if user is None or content is None:
        return "Access Denied"

    # Admins bypass subscription checks.
    if user.get("role", "").lower() == "admin":
        return content.get("title", "Access Denied")

    # Regular users must meet or exceed the required subscription level.
    user_level = _level_value(user.get("subscription_level", ""))
    content_level = _level_value(content.get("required_level", ""))

    if user_level >= content_level:
        return content.get("title", "Access Denied")

    # All other cases result in denial.
    return "Access Denied"