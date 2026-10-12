# -*- coding: utf-8 -*-
"""
Access control module for content delivery.
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"data": "Basic Article", "required_subscription": "basic"},
    102: {"data": "Premium Video", "required_subscription": "premium"},
}

# Define a simple subscription hierarchy for comparison
SUBSCRIPTION_LEVEL = {
    "basic": 1,
    "premium": 2,
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user is authorized, otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        Identifier of the user attempting to access the content.
    content_id : int
        Identifier of the content being accessed.

    Returns
    -------
    Any
        The 'data' field from CONTENT if access is granted, otherwise the string
        'Access Denied'.
    """
    # Retrieve user and content safely
    user = USERS.get(current_user_id)
    if not user:
        # Unknown user – deny access
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        # Unknown content – deny access
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["data"]

    # For regular users, verify subscription level
    user_level = SUBSCRIPTION_LEVEL.get(user.get("subscription", ""), 0)
    required_level = SUBSCRIPTION_LEVEL.get(content.get("required_subscription", ""), 0)

    if user_level >= required_level:
        return content["data"]

    # All other cases – deny access
    return "Access Denied"