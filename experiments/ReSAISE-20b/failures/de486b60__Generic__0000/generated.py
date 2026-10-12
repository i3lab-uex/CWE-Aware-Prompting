# -*- coding: utf-8 -*-

"""
Content access control module.

The global dictionaries `USERS` and `CONTENT` must be defined elsewhere in the
application. They map user IDs to role/subscription information and content
IDs to required subscription levels, respectively.

Example structure:

USERS = {
    1: {"role": "admin", "subscription_level": 3},
    2: {"role": "user",  "subscription_level": 1},
    ...
}

CONTENT = {
    101: {"title": "Premium Article",   "required_level": 2},
    102: {"title": "Basic Tutorial",     "required_level": 1},
    ...
}
"""

from typing import Dict, Any

# Assume these are provided by the application environment.
USERS: Dict[int, Dict[str, Any]] = {}
CONTENT: Dict[int, Dict[str, Any]] = {}


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    permissions; otherwise return 'Access Denied'.

    Parameters:
        uid (int): The ID of the user attempting to access content.
        cont_id (int): The ID of the requested content.

    Returns:
        str: The title of the content or 'Access Denied'.
    """
    # Retrieve user and content safely
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content.get("title", "Access Denied")

    # Regular users must have a subscription level >= required
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    if (
        isinstance(user_level, int)
        and isinstance(required_level, int)
        and user_level >= required_level
    ):
        return content.get("title", "Access Denied")

    return "Access Denied"