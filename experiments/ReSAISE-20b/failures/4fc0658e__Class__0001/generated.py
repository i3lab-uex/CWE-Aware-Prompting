# -*- coding: utf-8 -*-
"""
Content access control module.

This module defines a single function `fetch_content` that performs
authorization checks based on user role and subscription level.
"""

from typing import Dict

# ----------------------------------------------------------------------
# Sample data – in a real system these would be loaded from a database
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user",  "subscription_level": "basic"},
    3: {"role": "user",  "subscription_level": "free"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Intro to Python",        "required_level": "free"},
    102: {"title": "Advanced Algorithms",   "required_level": "basic"},
    103: {"title": "Quantum Computing",     "required_level": "premium"},
}

# ----------------------------------------------------------------------
# Subscription level hierarchy
# ----------------------------------------------------------------------
LEVEL_ORDER = {"free": 0, "basic": 1, "premium": 2}

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized
    to view it.  Otherwise, return 'Access Denied'.

    Parameters:
        given_user_id (int): The ID of the user requesting access.
        target_content_id (int): The ID of the content being requested.

    Returns:
        str: Content title or 'Access Denied'.
    """
    # 1. Retrieve user and content records
    user = USERS.get(given_user_id)
    content = CONTENT.get(target_content_id)

    # 2. Basic existence checks
    if user is None or content is None:
        return "Access Denied"

    # 3. Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # 4. Regular users must meet or exceed required level
    user_level = LEVEL_ORDER.get(user.get("subscription_level"), -1)
    required_level = LEVEL_ORDER.get(content.get("required_level"), -1)

    if user_level >= required_level:
        return content["title"]

    # 5. Deny otherwise
    return "Access Denied"