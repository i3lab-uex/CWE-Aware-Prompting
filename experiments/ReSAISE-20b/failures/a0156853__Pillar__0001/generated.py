# -*- coding: utf-8 -*-
"""
Author: ChatGPT
Date: 2026-07-23

This module provides a simple access control function that checks whether a user
is allowed to view a particular piece of content based on their role and
subscription level. The function follows the principle of least privilege,
ensuring that only authorized users can access restricted resources.

CWE-284: Improper Access Control
"""

from typing import Dict

# Example data structures. In a real application these would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Intro to Python", "required_subscription_level": "basic"},
    102: {"title": "Advanced AI Techniques", "required_subscription_level": "premium"},
    103: {"title": "Admin Dashboard", "required_subscription_level": "admin"},
}


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user is allowed to access a piece of content.

    Parameters
    ----------
    uid : int
        The user ID attempting to access the content.
    cid : int
        The content ID that the user wants to view.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise, "Access Denied".

    Notes
    -----
    - Admin users bypass all subscription checks.
    - For regular users, the user's subscription level must be at least as high
      as the content's required subscription level. The levels are compared
      lexicographically, assuming a simple hierarchy: 'basic' < 'premium'.
    - If either the user or content does not exist, access is denied.
    """
    # Retrieve user and content data safely
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Determine subscription level hierarchy
    level_order = {"basic": 1, "premium": 2}

    user_level_name = user.get("subscription_level")
    content_req_name = content.get("required_subscription_level")

    # Fallback: if levels are unknown, deny access
    user_level = level_order.get(user_level_name)
    content_req = level_order.get(content_req_name)

    if user_level is None or content_req is None:
        return "Access Denied"

    # Grant access if user's level meets or exceeds the required level
    if user_level >= content_req:
        return content["title"]

    return "Access Denied"