# -*- coding: utf-8 -*-

"""
Access control module.

This module defines a single function `access_content` that checks whether
a user is authorized to view a particular piece of content.  The function
performs an explicit authorization check using the user’s role and
subscription level, mitigating CWE‑862 (Missing Authorization).

The data structures `USERS` and `CONTENT` are expected to be provided
elsewhere in the application.  They can be simple dictionaries for
illustration purposes:

    USERS = {
        user_id: {"role": "admin" | "user", "subscription": "basic" | "premium"},
        ...
    }

    CONTENT = {
        content_id: {"data": ..., "required_subscription": "basic" | "premium"},
        ...
    }
"""

from typing import Any, Dict

# Example data structures – replace with actual application data
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"data": "Public article", "required_subscription": "basic"},
    102: {"data": "Premium video", "required_subscription": "premium"},
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user has sufficient privileges,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        Identifier of the user attempting to access content.
    content_id : int
        Identifier of the content being requested.

    Returns
    -------
    Any
        The content data if authorized, or the string 'Access Denied'.
    """
    # 1. Validate input types
    if not isinstance(current_user_id, int) or not isinstance(content_id, int):
        return "Access Denied"

    # 2. Retrieve user record
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    # 3. Retrieve content record
    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # 4. Authorization logic
    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["data"]

    # Regular users must have a subscription that meets or exceeds
    # the required level.  For simplicity we define an ordering.
    subscription_order = {"basic": 1, "premium": 2}
    user_level = subscription_order.get(user.get("subscription"), 0)
    required_level = subscription_order.get(content.get("required_subscription"), 0)

    if user_level >= required_level:
        return content["data"]

    # If none of the conditions match, deny access
    return "Access Denied"