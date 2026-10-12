# -*- coding: utf-8 -*-
"""
Module providing access control for content based on user subscription level.

Author: OpenAI
"""

from typing import Dict, Any

# Sample data – in a real application these would come from a database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"required_subscription": "basic", "data": "Basic Article"},
    102: {"required_subscription": "premium", "data": "Premium Video"},
    103: {"required_subscription": None, "data": "Open Resource"},  # accessible to all
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user is authorized; otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access the content.
    content_id : int
        The identifier of the requested content.

    Returns
    -------
    Any
        The content data if access is permitted; otherwise the string 'Access Denied'.

    Notes
    -----
    * Admin users can access any content.
    * Regular users may only access content that matches their subscription level.
    * Content with ``required_subscription`` set to ``None`` is public and accessible
      by all users.
    """
    # Fetch user and content safely; if either is missing, deny access
    user = USERS.get(current_user_id)
    content = CONTENT.get(content_id)

    if not user or not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["data"]

    # Public content is accessible to everyone
    required_sub = content.get("required_subscription")
    if required_sub is None:
        return content["data"]

    # For regular users, subscription must match
    user_sub = user.get("subscription")
    if user_sub == required_sub:
        return content["data"]

    # All other cases: deny access
    return "Access Denied"